// Define our core types
export interface LLMResponse {
    model: string;
    response: string;
    metrics: ModelMetrics;
}

export interface Experiment {
    id: string;
    prompt: string;
    responses: LLMResponse[];
    models: string[];
}

export interface Metrics {
  avgResponseTime: number;
  avgAccuracy: number;
  avgRelevancy: number;
  count: number;
}

export interface ModelMetrics {
    responseTime: number;
    accuracy?: number;
    relevancy?: number;
}

export interface ModelPerformance {
    [key: string]: {
        avgResponseTime: number;
        avgAccuracy: number;
        avgRelevancy: number;
        count: number;
    };
}

export interface ChartDataPoint {
    model: string;
    responseTime: number;
    accuracy: number;
    relevancy: number;
}

export interface LoadingState {
  [key: string]: boolean;
}