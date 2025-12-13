
'use client';

import { useState, useEffect } from 'react';
import { api, Word, PracticeResult } from '@/lib/api';
import WordCard from '@/components/WordCard';
import PracticeForm from '@/components/PracticeForm';
import ResultCard from '@/components/ResultCard';

export default function PracticePage() {
  const [word, setWord] = useState<Word | null>(null);
  const [result, setResult] = useState<PracticeResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const loadWord = async () => {
    try {
      setLoading(true);
      setError('');
      setResult(null);
      const data = await api.getRandomWord();
      setWord(data);
    } catch (err) {
      console.error('Error loading word:', err);
      setError(err instanceof Error ? err.message : 'Failed to load word. Please check if the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (sentence: string) => {
    if (!word) return;

    try {
      setLoading(true);
      setError('');
      const data = await api.submitPractice(word.id, sentence);
      setResult(data);
    } catch (err) {
      console.error('Error submitting practice:', err);
      setError(err instanceof Error ? err.message : 'Failed to validate sentence. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadWord();
  }, []);

  return (
    <div>
      <h2>Practice Your English</h2>
      
      {error && (
        <div className="error">
          <strong>Error:</strong> {error}
        </div>
      )}
      
      {loading && !word && (
        <div className="card">
          <div className="loading">Loading word</div>
        </div>
      )}
      
      {word && (
        <>
          <WordCard word={word} />
          <div className="card">
            <PracticeForm onSubmit={handleSubmit} loading={loading} />
          </div>
          {result && <ResultCard result={result} />}
          <button
            onClick={loadWord}
            className="button button-primary"
            style={{ marginTop: '1rem', width: '100%' }}
            disabled={loading}
          >
            {loading ? 'Loading...' : 'Next Word →'}
          </button>
        </>
      )}
    </div>
  );
}
