
'use client';

import { useState } from 'react';

interface PracticeFormProps {
  onSubmit: (sentence: string) => void;
  loading: boolean;
}

export default function PracticeForm({ onSubmit, loading }: PracticeFormProps) {
  const [sentence, setSentence] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (sentence.trim()) {
      onSubmit(sentence);
      setSentence('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="practice-form">
      <textarea
        value={sentence}
        onChange={(e) => setSentence(e.target.value)}
        placeholder="Write a sentence using this word..."
        disabled={loading}
        rows={4}
        required
      />
      <button type="submit" disabled={loading || !sentence.trim()}>
        {loading ? 'Validating...' : 'Submit'}
      </button>
    </form>
  );
}
