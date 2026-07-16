import { redirect } from 'next/navigation';
import { PageShell } from '@/components/page-shell';
import { prisma } from '@/lib/db';
import { createInvite } from '@/lib/invites';
import { sendInviteEmail } from '@/lib/mailer';
import { getCurrentUser } from '@/lib/session';
import { appUrl } from '@/lib/config';

async function createInviteAction(formData: FormData) {
  'use server';
  const admin = await getCurrentUser();
  if (!admin || !['admin', 'ceo'].includes(admin.role)) redirect('/login');
  const name = String(formData.get('name') || '').trim();
  const email = String(formData.get('email') || '').trim().toLowerCase();
  const role = String(formData.get('role') || 'employee') as 'employee' | 'admin' | 'ceo';
  if (!name || !email) redirect('/admin/users?error=missing');
  const invite = await createInvite({ name, email, role, createdById: admin.id });
  await sendInviteEmail(email, name, `${appUrl()}/invite/${invite.token}`);
  redirect('/admin/users?sent=1');
}

export default async function AdminUsersPage() {
  const user = await getCurrentUser();
  if (!user) redirect('/login');
  if (!['admin', 'ceo'].includes(user.role)) redirect('/dashboard');
  const users = await prisma.user.findMany({ orderBy: { createdAt: 'desc' } });
  const invites = await prisma.invite.findMany({ orderBy: { createdAt: 'desc' }, take: 10 });
  return (
    <PageShell title="Users" description="Invite new hires and review role assignments.">
      <div className="grid gap-6 lg:grid-cols-[1fr_1.2fr]">
        <div className="card p-6">
          <h2 className="text-lg font-semibold text-slate-900">Send invite</h2>
          <form action={createInviteAction} className="mt-4 space-y-4">
            <div><label className="mb-2 block text-sm font-medium text-slate-700">Name</label><input className="input" name="name" required /></div>
            <div><label className="mb-2 block text-sm font-medium text-slate-700">Email</label><input className="input" name="email" type="email" required /></div>
            <div><label className="mb-2 block text-sm font-medium text-slate-700">Role</label><select className="input" name="role" defaultValue="employee"><option value="employee">Employee</option><option value="admin">Admin</option><option value="ceo">CEO</option></select></div>
            <button className="button w-full" type="submit">Create invite and email link</button>
          </form>
        </div>
        <div className="space-y-6">
          <div className="card overflow-hidden">
            <div className="border-b border-slate-200 px-6 py-4 font-semibold text-slate-900">Current users</div>
            <table className="min-w-full divide-y divide-slate-200 text-sm"><tbody className="divide-y divide-slate-200 bg-white">{users.map((u) => (<tr key={u.id}><td className="px-6 py-4 font-medium text-slate-900">{u.name}</td><td className="px-6 py-4 text-slate-600">{u.email}</td><td className="px-6 py-4 capitalize text-slate-600">{u.role}</td><td className="px-6 py-4 text-slate-600">{u.active ? 'Active' : 'Inactive'}</td></tr>))}</tbody></table>
          </div>
          <div className="card overflow-hidden">
            <div className="border-b border-slate-200 px-6 py-4 font-semibold text-slate-900">Recent invites</div>
            <table className="min-w-full divide-y divide-slate-200 text-sm"><tbody className="divide-y divide-slate-200 bg-white">{invites.map((invite) => (<tr key={invite.id}><td className="px-6 py-4 font-medium text-slate-900">{invite.name}</td><td className="px-6 py-4 text-slate-600">{invite.email}</td><td className="px-6 py-4 text-slate-600">{invite.usedAt ? 'Used' : 'Pending'}</td><td className="px-6 py-4 text-slate-600"><a href={`/invite/${invite.token}`}>Invite link</a></td></tr>))}</tbody></table>
          </div>
        </div>
      </div>
    </PageShell>
  );
}
