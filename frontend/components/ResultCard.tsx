/**
 * ════════════════════════════════════════════════════════════════
 * Practice Result Display
 * ════════════════════════════════════════════════════════════════
 */
import { PracticeResult } from '@/lib/api';

export default function ResultCard({ result }: { result: PracticeResult }) {
  const getScoreColor = (score: number) => {
    if (score >= 8) return '#10b981';
    if (score >= 6) return '#f59e0b';
    return '#ef4444';
  };

  return (
    <div className="result-card">
      <div className="score" style={{ color: getScoreColor(result.score) }}>
        Score: {result.score}/10
      </div>
      <div className="level">Level: {result.cefr_level}</div>
      <p className="feedback">{result.feedback}</p>
      {result.corrected_sentence && (
        <p className="correction">
          <strong>Suggestion:</strong> {result.corrected_sentence}
        </p>
      )}
    </div>
  );
}
