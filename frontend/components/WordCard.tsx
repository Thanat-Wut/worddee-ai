
import { Word } from '@/lib/api';

interface WordCardProps {
  word: Word;
}

export default function WordCard({ word }: WordCardProps) {
  return (
    <div className="card word-card">
      <h2 className="word">{word.word}</h2>
      <p className="definition">{word.definition}</p>
      <span className="badge">{word.difficulty_level}</span>
    </div>
  );
}
