import React, { useState } from 'react';
import { TextField, Button, Box, Paper } from '@mui/material';
import ModelSelector from './ModelSelector';

interface PromptInputProps {
  onSubmit: (data: { prompt: string; systemPrompt: string; models: string[] }) => void;
  loading?: boolean;
}

const AVAILABLE_MODELS = ['mixtral-8x7b', 'gpt-2'];

const PromptInput: React.FC<PromptInputProps> = ({ onSubmit, loading }) => {
  const [prompt, setPrompt] = useState('');
  const [systemPrompt, setSystemPrompt] = useState('');
  const [selectedModels, setSelectedModels] = useState<string[]>([]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (prompt && selectedModels.length > 0) {
      onSubmit({
        prompt,
        systemPrompt,
        models: selectedModels
      });
    }
  };

  return (
    <Paper sx={{ p: 3, mb: 3 }}>
      <form onSubmit={handleSubmit}>
        <ModelSelector
          availableModels={AVAILABLE_MODELS}
          selectedModels={selectedModels}
          onChange={setSelectedModels}
        />
        <TextField
          fullWidth
          label="System Prompt (Optional)"
          value={systemPrompt}
          onChange={(e) => setSystemPrompt(e.target.value)}
          margin="normal"
          multiline
          rows={2}
        />
        <TextField
          fullWidth
          required
          label="User Prompt"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          margin="normal"
          multiline
          rows={4}
        />
        <Box sx={{ mt: 2 }}>
          <Button 
            type="submit" 
            variant="contained" 
            disabled={loading || !prompt || selectedModels.length === 0}
            fullWidth
          >
            {loading ? 'Evaluating...' : 'Evaluate Models'}
          </Button>
        </Box>
      </form>
    </Paper>
  );
};

export default PromptInput;