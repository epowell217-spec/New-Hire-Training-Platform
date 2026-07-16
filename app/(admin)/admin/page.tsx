import Link from 'next/link';
import { redirect } from 'next/navigation';
import { PageShell } from '@/components/page-shell';
import { getCurrentUser } from '@/lib/session';

export default async function AdminHome() {
  const user = await getCurrentUser();
  if (!user) redirect('/login');
  if (!['admin', 'ceo'].includes(user.role)) redirect('/dashboard');
  return (
    <PageShell title="Admin dashboard" description="Manage modules, welcome video, and users.">
      <div className="grid gap-4 md:grid-cols-3">
        <Link href="/admin/modules" className="card p-5 hover:border-brand-500"><h3 className="font-semibold text-slate-900">Training modules</h3><p className="mt-1 text-sm text-slate-600">Add or edit compliance lessons.</p></Link>
        <Link href="/admin/welcome-video" className="card p-5 hover:border-brand-500"><h3 className="font-semibold text-slate-900">CEO welcome video</h3><p className="mt-1 text-sm text-slate-600">Upload a welcome video without code changes.</p></Link>
        <Link href="/admin/users" className="card p-5 hover:border-brand-500"><h3 className="font-semibold text-slate-900">New hires</h3><p className="mt-1 text-sm text-slate-600">Invite users and review statuses.</p></Link>
      </div>
    </PageShell>
  );
}
