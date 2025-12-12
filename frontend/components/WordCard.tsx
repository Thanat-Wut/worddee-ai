/**
 * ════════════════════════════════════════════════════════════════
 * Word Display Card Component
 * ════════════════════════════════════════════════════════════════
 */
import { Word } from '@/lib/api';

export default function WordCard({ word }: { word: Word }) {
  return (
    <div className="card">
      <h2 className="word">{word.word}</h2>
      {word.pronunciation && (
        <p className="pronunciation">{word.pronunciation}</p>
      )}
      <p className="definition">{word.definition}</p>
      {word.example_sentence && (
        <p className="example">Example: {word.example_sentence}</p>
      )}
      <span className="badge">{word.difficulty_level}</span>
    </div>
  );
}
