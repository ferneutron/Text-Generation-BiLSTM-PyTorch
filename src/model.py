import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

class TextGenerator(nn.ModuleList):
	def __init__(self):
		super(TextGenerator, self).__init__()
		
		self.batch_size = 2
		self.hidden_dim = 128
		self.input_size = 35
		self.num_classes = 35
		self.sequence_len = 4
		
		self.embedding = nn.Embedding(self.input_size, self.hidden_dim, padding_idx=0)
		self.lstm_cell_1 = nn.LSTMCell(self.hidden_dim, self.hidden_dim)
		self.lstm_cell_2 = nn.LSTMCell(self.hidden_dim, self.hidden_dim)
		self.fc_1 = nn.Linear(self.hidden_dim, self.num_classes)
		
		self.softmax = nn.Softmax(dim=1)
		
	def forward(self, x):
	
		# batch_size x hidden_size
		hidden_state = torch.zeros(self.batch_size, self.hidden_dim)
		cell_state = torch.zeros(self.batch_size, self.hidden_dim)

		# weights initialization
		torch.nn.init.xavier_normal_(hidden_state)
		torch.nn.init.xavier_normal_(cell_state)
		
		# From idx to embedding
		out = self.embedding(x)
		
		# Prepare the shape for LSTMCell
		out = out.view(self.sequence_len, self.batch_size, -1)

		# Unfolding LSTM
		# Last hidden_state will be used to feed the fully connected neural net
		for i in range(self.sequence_len):
		 	hidden_state, cell_state = self.lstm_cell_1(out[i], (hidden_state, cell_state))
		 	
		# Last hidden state is passed through a fully connected neural net
		out = self.fc_1(hidden_state)
		
		# Softmax activation function
		out = self.softmax(out)
		
		return out
		
		