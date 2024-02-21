
# https://medium.com/@sntaus/building-a-mini-gpt-like-language-model-from-scratch-27257bf5c145

# pip install torch
import torch
import torch.nn as nn
import torch.optim as optim
import pprint

# Function to obtain training data, vocab and mapping from word to index and vice versa
def get_data_and_vocab():
    # Define training data
    training_data = {
        "how are you": "i am fine <end>",
        "who is john": "a nice person <end>",
        "who is nice": "john <end>",
        "where is john": "at home <end>",
        "how is john": "i dont know <end>",
        "who are you": "mini gpt model <end>"
    }
    
    # Extract input and target phrases
    data_words = [k for k, _ in training_data.items()]
    target_words = [v for _, v in training_data.items()]
    
    # Build vocabulary from training data
    vocabulary_words = list(set([element.lower() for nestedlist in [x.split(" ") for x in data_words] for element in nestedlist] + [element.lower() for nestedlist in [x.split(" ") for x in target_words] for element in nestedlist]))
    
    # Ensure <end> token is at the end of vocabulary list, and there's a blank at the beginning
    vocabulary_words.remove("<end>")
    vocabulary_words.append("<end>")
    vocabulary_words.insert(0, "")
    
    # Create mappings from word to index and index to word
    word_to_ix = {vocabulary_words[k].lower(): k for k in range(len(vocabulary_words))}
    ix_to_word = {v: k for k, v in word_to_ix.items()}
    
    # Return all the necessary data and mappings
    return training_data, data_words, target_words, vocabulary_words, word_to_ix, ix_to_word

# Function to convert a batch of sequences of words to a tensor of indices
def words_to_tensor(seq_batch, device=None):
    index_batch = []
    
    # Loop over sequences in the batch
    for seq in seq_batch:
        word_list = seq.lower().split(" ")
        indices = [word_to_ix[word] for word in word_list if word in word_to_ix]
        t = torch.tensor(indices)
        if device is not None:
            t = t.to(device)  # Transfer tensor to the specified device
        index_batch.append(t)
    
    # Pad tensors to have the same length
    return pad_tensors(index_batch)

# Function to convert a tensor of indices to a list of sequences of words
def tensor_to_words(tensor):
    index_batch = tensor.cpu().numpy().tolist()
    res = []
    for indices in index_batch:
        words = []
        for ix in indices:
            words.append(ix_to_word[ix].lower())  # Convert index to word
            if ix == word_to_ix["<end>"]:
                break  # Stop when <end> token is encountered
        res.append(" ".join(words))
    return res

# Function to pad a list of tensors to the same length
def pad_tensors(list_of_tensors):
    tensor_count = len(list_of_tensors) if not torch.is_tensor(list_of_tensors) else list_of_tensors.shape[0]
    max_dim = max(t.shape[0] for t in list_of_tensors)  # Find the maximum length
    res = []
    for t in list_of_tensors:
        # Create a zero tensor of the desired shape
        res_t = torch.zeros(max_dim, *t.shape[1:]).type(t.dtype).to(t.device)
        res_t[:t.shape[0]] = t  # Copy the original tensor into the padded tensor
        res.append(res_t)
    
    # Concatenate tensors along a new dimension
    res = torch.cat(res)
    firstDim = len(list_of_tensors)
    secondDim = max_dim
    
    # Reshape the result to have the new dimension first
    return res.reshape(firstDim, secondDim, *res.shape[1:])

# Define Self-Attention module
class SelfAttention(nn.Module):
    def __init__(self, embed_size, head_count):
        super(SelfAttention, self).__init__()
        self.embed_size = embed_size  # Size of word embeddings
        self.head_count = head_count  # Number of attention heads
        
        # Create linear layers for query, key and value projections for each head
        self.query_layers = nn.ModuleList([nn.Linear(embed_size, embed_size, bias=False) for _ in range(head_count)])
        self.key_layers = nn.ModuleList([nn.Linear(embed_size, embed_size, bias=False) for _ in range(head_count)])
        self.value_layers = nn.ModuleList([nn.Linear(embed_size, embed_size, bias=False) for _ in range(head_count)])
        self.fc_out = nn.Linear(head_count * embed_size, embed_size)  # Final linear layer to combine head outputs

    def forward(self, embeddings):
        batch_size, token_count = embeddings.shape[:2]
        qkvs = torch.zeros(self.head_count, 3, batch_size, token_count, self.embed_size).to(embeddings.device)
        
        # Loop over heads and compute query, key and value projections
        for i in range(self.head_count):
            qkvs[i, 0] = self.query_layers[i](embeddings)
            qkvs[i, 1] = self.key_layers[i](embeddings)
            qkvs[i, 2] = self.value_layers[i](embeddings)
        
        # Compute energy terms for each head, batch, and pair of tokens
        energy = torch.zeros(self.head_count, batch_size, token_count, token_count).to(embeddings.device)
        # Create a mask with false on and below the diagonal, and true above the diagonal
        mask = torch.triu(torch.ones((token_count, token_count)), diagonal=1).bool()
        
        for h in range(self.head_count):
            for b in range(batch_size):
                for i in range(token_count):
                    for j in range(token_count):
                        energy[h, b, i, j] = torch.dot(qkvs[h, 0, b, i], qkvs[h, 1, b, j])
                energy[h, b] = energy[h, b].masked_fill(mask, float('-inf')) # Apply mask
        
        # Compute attention scores
        attention = torch.nn.functional.softmax(energy, dim=3)
        
        # Compute weighted sum of values for each head and token
        out = torch.zeros(batch_size, token_count, self.head_count, self.embed_size).to(embeddings.device)
        for h in range(self.head_count):
            for b in range(batch_size):
                for i in range(token_count):
                    for j in range(token_count):
                        out[b, i, h] += (attention[h, b, i, j] * qkvs[h, 2, b, j])
        
        # Reshape and pass through final linear layer
        out = out.reshape(batch_size, token_count, self.head_count * self.embed_size)
        return self.fc_out(out)
    
    def masked_attention(self, energy):
        # Assume scores has shape (batch_size, max_token_count, embed_size, embed_size)
        max_token_count, embed_size, _ = energy.size()

        # Create a mask with zeros on and below the diagonal, and negative infinity above the diagonal
        mask = torch.triu(torch.ones((max_token_count, max_token_count)), diagonal=1) * float('-inf')
        mask = mask.unsqueeze(0).unsqueeze(0)  # Add dimensions for batch and embedding size
        mask = mask.expand(batch_size, embed_size, -1, -1)  # Expand mask to match batch and embedding size

        # Apply the mask to the scores
        masked_scores = energy + mask.to(energy.device)

        return masked_scores.to(energy.device)

# Define Transformer block module
class TransformerBlock(nn.Module):
    def __init__(self, embed_size, head_count):
        super(TransformerBlock, self).__init__()
        self.attention = SelfAttention(embed_size, head_count)  # Self-attention layer
        self.norm1 = nn.LayerNorm(embed_size)  # Layer normalization
        self.norm2 = nn.LayerNorm(embed_size)  # Layer normalization
        
        # Feed-forward neural network
        self.feed_forward = nn.Sequential(
            nn.Linear(embed_size, embed_size),
            nn.ReLU(),
            nn.Linear(embed_size, embed_size)
        )
    
    def forward(self, embeddings):
        attention = self.attention(embeddings)
        
        # Apply residual connections and layer normalization
        out = self.norm1(attention + embeddings)
        out = attention + self.feed_forward(out)
        out = self.norm2(out)
        return out

# Define Transformer module
class Transformer(nn.Module):
    def __init__(self, vocab_size, embed_size, num_layers, head_count):
        super(Transformer, self).__init__()
        self.embed_size = embed_size  # Size of word embeddings
        self.vocab_size = vocab_size  # Size of vocabulary
        self.word_embedding = nn.Embedding(vocab_size, embed_size)  # Embedding layer
        
        # List of transformer blocks
        self.layers = nn.ModuleList(
            [TransformerBlock(embed_size, head_count) for _ in range(num_layers)]
        )
        self.fc_out = nn.Linear(embed_size, vocab_size)  # Final linear layer to produce logits

    def forward(self, input_tokens, mask=None):
        batch_size, token_count = input_tokens.shape[:2]
        out = self.word_embedding(input_tokens)  # Obtain word embeddings
        
        # Compute position encodings and add to word embeddings
        positions = torch.arange(0, token_count).expand(batch_size, token_count).to(input_tokens.device)
        position_encoding = self.position_encoding(positions, self.embed_size)
        out += position_encoding.reshape(out.shape)
        
        # Pass through each transformer block
        for layer in self.layers:
            out = layer(out)
        
        # Produce logits for the final token in each sequence
        out = self.fc_out(out[:, -1, :].reshape(batch_size, self.embed_size)).reshape(batch_size, self.vocab_size)
        return torch.nn.functional.softmax(out, dim=1)  # Apply softmax to obtain probabilities

    def position_encoding(self, positions, embed_size):
        # Compute position encoding for each position and dimension
        angle_rads = self.get_angles(
            positions.unsqueeze(2).float(), 
            torch.arange(embed_size)[None, None, :].float().to(positions.device), 
            embed_size
        )
        sines = torch.sin(angle_rads[:, :, 0::2])  # Compute sine of angle for even dimensions
        cosines = torch.cos(angle_rads[:, :, 1::2])  # Compute cosine of angle for odd dimensions
        pos_encoding = torch.cat([sines, cosines], dim=-1)  # Concatenate sine and cosine values
        pos_encoding = pos_encoding[None, ...]
        return pos_encoding

    def get_angles(self, pos, i, embed_size):
        # Compute angle rate for each position and dimension
        angle_rates = 1 / torch.pow(10000, (2 * (i//2)) / embed_size)
        return pos * angle_rates

# Function to train the model recursively over each sequence and token
def train_recursive(model, data, targets, optimizer, criterion):
    model.train()  # Set model to training mode
    optimizer.zero_grad()  # Zero the gradients
    total_loss = 0  # Initialize total loss
    batch_size, token_count, token_count_out = data.shape[0], data.shape[1], targets.shape[1]
    
    # Loop over sequences in the batch
    for b in range(batch_size):
        end_encountered = False
        cur_count = 0
        # Loop over tokens in the sequence
        while not end_encountered:
            target_vector = torch.zeros(model.vocab_size).to(data.device)  # Initialize target vector

            if cur_count != token_count_out:
                expected_next_token_idx = targets[b, cur_count]  # Get index of expected next token
                target_vector[expected_next_token_idx] = 1  # Set the corresponding element of the target vector to 1
            
            # Concatenate current input and output tokens and pass through model
            if cur_count > 0:
                model_input = data[b].reshape(token_count).to(data.device)
                part_of_output = targets[b, :cur_count].to(data.device)
                model_input = torch.cat((model_input, part_of_output))
            else:
                model_input = data[b]
            out = model(model_input.reshape(1, token_count + cur_count))
            
            # Compute loss and accumulate total loss
            loss = criterion(out, target_vector.reshape(out.shape))
            total_loss += loss
            cur_count += 1
            
            # Stop when the end of the sequence is reached
            if cur_count > token_count_out:
                end_encountered = True
    
    # Backpropagate gradients and update model parameters
    total_loss.backward()
    optimizer.step()
    return total_loss.item() / batch_size

# Function to perform inference recursively for each sequence in a batch
def infer_recursive(model, input_vectors, max_output_token_count=10):
    model.eval()  # Set model to evaluation mode
    outputs = []

    # Loop over sequences in the batch
    for i in range(input_vectors.shape[0]):
        print(f"Infering sequence {i}")
        input_vector = input_vectors[i].reshape(1, input_vectors.shape[1])
        predicted_sequence = []
        wc = 0  # Initialize word count

        with torch.no_grad():  # Disable gradient computation
            while True:
                output = model(input_vector)  # Pass current input through model
                predicted_index = output[0, :].argmax().item()  # Get index of predicted token
                predicted_sequence.append(predicted_index)  # Append predicted index to sequence
                # Stop when <end> token is predicted or the maximum output length is reached
                if predicted_index == word_to_ix['<end>'] or wc > max_output_token_count:
                    break
                # Append predicted token to input and increment word count
                input_vector = torch.cat([input_vector, torch.tensor([[predicted_index]])], dim=1)
                wc += 1
        outputs.append(torch.tensor(predicted_sequence))  # Append predicted sequence to outputs
    outputs = pad_tensors(outputs)  # Pad predicted sequences to the same length
    return outputs

# Function to demonstrate training and inference
def example_training_and_inference():
    # Get model hyperparameters from vocabulary size
    vocab_size = len(word_to_ix)
    embed_size = 512
    num_layers = 4
    heads = 3

    # Create model, optimizer, and loss function
    device = torch.device("cpu")
    model = Transformer(vocab_size, embed_size, num_layers, heads).to(device)
    optimizer = optim.Adam(model.parameters(), lr=0.00001)
    criterion = nn.CrossEntropyLoss()

    # Convert training data to tensors
    data = words_to_tensor(data_words, device=device)
    targets = words_to_tensor(target_words, device=device)

    # Train model for 55 epochs
    for epoch in range(55):
        avg_loss = train_recursive(model, data, targets, optimizer, criterion)
        print(f'Epoch {epoch + 1}, Loss: {avg_loss:.4f}')

    # Perform inference on training data
    input_vector = words_to_tensor(data_words, device=device)
    predicted_vector = infer_recursive(model, input_vector)
    predicted_words = tensor_to_words(predicted_vector)

    # Print training data and model output
    print("\n\n\n")
    print("Training Data:")
    pprint.pprint(training_data)
    print("\n\n")
    print("Model Inference:")
    result_data = {data_words[k]: predicted_words[k] for k in range(len(predicted_words))}
    pprint.pprint(result_data)

# Main function to call the demonstration function
if __name__ == "__main__":
    # Get training data and vocabulary
    training_data, data_words, target_words, vocabulary_words, word_to_ix, ix_to_word = get_data_and_vocab()
    # Run the example training and inference function
    example_training_and_inference()