

const BACKEND_URL = process.env.NEXT_PUBLIC_WORDDEE_API_URL || 'http://localhost:8000';

export interface Word {
  id: number;
  word: string;
  definition: string;
  difficulty_level: string;
  created_at: string;
}

export interface PracticeResult {
  session_id: number;
  word_id: number;
  user_sentence: string;
  score: number;
  cefr_level: string;
  feedback: string;
  corrected_sentence?: string;
  practiced_at: string;
}

export interface DashboardStats {
  total_sessions: number;
  average_score: number;
  most_common_level: string;
  recent_sessions: PracticeResult[];
}

class APIError extends Error {
  constructor(message: string, public status?: number) {
    super(message);
    this.name = 'APIError';
  }
}

export const api = {
  
  async getRandomWord(difficulty?: string): Promise<Word> {
    try {
      const params = difficulty ? `?difficulty=${difficulty}` : '';
      const res = await fetch(`${BACKEND_URL}/api/practice/word${params}`);
      if (!res.ok) {
        throw new APIError(`Failed to fetch word: ${res.statusText}`, res.status);
      }
      return res.json();
    } catch (error) {
      if (error instanceof APIError) throw error;
      throw new APIError('Network error: Could not connect to server');
    }
  },

  
  async submitPractice(wordId: number, sentence: string): Promise<PracticeResult> {
    try {
      const res = await fetch(`${BACKEND_URL}/api/practice/submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          word_id: wordId,
          user_sentence: sentence,
        }),
      });
      if (!res.ok) {
        throw new APIError(`Failed to submit practice: ${res.statusText}`, res.status);
      }
      return res.json();
    } catch (error) {
      if (error instanceof APIError) throw error;
      throw new APIError('Network error: Could not connect to server');
    }
  },

  
  async getDashboardStats(): Promise<DashboardStats> {
    try {
      const res = await fetch(`${BACKEND_URL}/api/dashboard/stats`);
      if (!res.ok) {
        throw new APIError(`Failed to fetch stats: ${res.statusText}`, res.status);
      }
      return res.json();
    } catch (error) {
      if (error instanceof APIError) throw error;
      throw new APIError('Network error: Could not connect to server');
    }
  },
};
