import Link from 'next/link';
import { TrainingModule } from '@/lib/types';

export function ModuleCard({ module }: { module: TrainingModule & { completed?: boolean } }) {
  return (
    <div className="card p-5">
      <div className="mb-2 flex items-start justify-between gap-4">
        <div>
          <h3 className="text-lg font-semibold text-slate-900">{module.title}</h3>
          <p className="text-sm text-slate-500">{module.description}</p>
        </div>
        <span className={module.completed ? 'rounded-full bg-emerald-100 px-3 py-1 text-xs font-medium text-emerald-700' : 'rounded-full bg-amber-100 px-3 py-1 text-xs font-medium text-amber-700'}>
          {module.completed ? 'Completed' : 'Pending'}
        </span>
      </div>
      <div className="mt-4 flex items-center justify-between">
        <span className="text-sm text-slate-500">{module.required ? 'Required' : 'Optional'}</span>
        <Link className="button" href={`/training/${module.id}`}>Open</Link>
      </div>
    </div>
  );
}
