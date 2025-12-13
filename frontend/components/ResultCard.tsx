
import { PracticeResult } from '@/lib/api';

interface ResultCardProps {
  result: PracticeResult;
}

export default function ResultCard({ result }: ResultCardProps) {
  const getScoreClass = (score: number) => {
    if (score >= 9) return 'excellent';
    if (score >= 7) return 'good';
    if (score >= 5) return 'fair';
    return 'poor';
  };

  const getScoreMessage = (score: number) => {
    if (score >= 9) return 'Excellent! 🎉';
    if (score >= 7) return 'Good job! 👍';
    if (score >= 5) return 'Not bad! 💪';
    return 'Keep practicing! 📚';
  };

  return (
    <div className="card result-card">
      <div className="score-display">
        <div className={`score-number ${getScoreClass(result.score)}`}>
          {result.score.toFixed(1)}
        </div>
        <div style={{ marginBottom: '1rem', fontSize: '1.25rem', fontWeight: 600 }}>
          {getScoreMessage(result.score)}
        </div>
        <span className="cefr-level">
          CEFR Level: {result.cefr_level}
        </span>
      </div>

      <div className="feedback-section">
        <h3>📝 Feedback</h3>
        <div className="feedback-text">
          {result.feedback}
        </div>
      </div>

      {result.corrected_sentence && result.corrected_sentence !== result.user_sentence && (
        <div className="sentence-comparison">
          <div className="sentence-box">
            <h4>Your Sentence</h4>
            <p>{result.user_sentence}</p>
          </div>
          <div className="sentence-box">
            <h4>Suggested Correction</h4>
            <p>{result.corrected_sentence}</p>
          </div>
        </div>
      )}
    </div>
  );
}
