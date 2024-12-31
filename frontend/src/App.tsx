import React, { useState } from 'react';
import { Container, Box, Typography, Alert, Snackbar } from '@mui/material';
import { submitPrompt } from './services/api';
import { Experiment, ModelPerformance } from './types/types';
import PromptInput from './components/PromptInput';
import ResponseComparison from './components/ResponseComparison';
import MetricsDashboard from './components/MetricsDashboard';

const App: React.FC = () => {
  const [experiments, setExperiments] = useState<Experiment[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (data: { prompt: string; systemPrompt: string; models: string[] }) => {
      setLoading(true);
      setError(null);
      try {
          const result = await submitPrompt(data);
          setExperiments([result]);
      } catch (error) {
          console.error('Error submitting prompt:', error);
          setError('Failed to evaluate prompt');
      } finally {
          setLoading(false);
      }
  };

  const calculateModelPerformance = (experiments: Experiment[]): ModelPerformance => {
    if (experiments.length === 0) return {};
    
    const performance: ModelPerformance = {};
    
    experiments.forEach(exp => {
      exp.models.forEach((model, idx) => {
        if (!performance[model]) {
          performance[model] = {
            avgResponseTime: 0,
            avgAccuracy: 0,
            avgRelevancy: 0,
            count: 0
          };
        }
        
        const response = exp.responses[idx];
        if (response?.metrics) {
          performance[model] = {
            avgResponseTime: response.metrics.responseTime,
            avgAccuracy: response.metrics.accuracy || 0,
            avgRelevancy: response.metrics.relevancy || 0,
            count: 1
          };
        }
      });
    });
    
    return performance;
  };

    return (
        <Container maxWidth="lg">
            <Box sx={{ my: 4 }}>
                <Typography variant="h4" component="h1" gutterBottom>
                    LLM Evaluation Platform
                </Typography>
                
                <PromptInput 
                    onSubmit={handleSubmit}
                    loading={loading}
                />
                
                {experiments.length > 0 && (
                    <>
                        <Typography variant="h5" sx={{ mt: 4, mb: 2 }}>
                            Results
                        </Typography>
                        <ResponseComparison experiments={experiments} />
                        <Box sx={{ mt: 4 }}>
                            <MetricsDashboard modelPerformance={calculateModelPerformance(experiments)} />
                        </Box>
                    </>
                )}

                <Snackbar 
                    open={!!error} 
                    autoHideDuration={6000} 
                    onClose={() => setError(null)}
                >
                    <Alert severity="error" onClose={() => setError(null)}>
                        {error}
                    </Alert>
                </Snackbar>
            </Box>
        </Container>
    );
};

export default App;