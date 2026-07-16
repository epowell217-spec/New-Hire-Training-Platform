import bcrypt from 'bcryptjs';
import { notFound, redirect } from 'next/navigation';
import { PageShell } from '@/components/page-shell';
import { getInviteByToken } from '@/lib/invites';
import { prisma } from '@/lib/db';
import { createSessionToken, setSessionCookie } from '@/lib/session';

async function acceptInviteAction(token: string, formData: FormData) {
  'use server';
  const invite = await getInviteByToken(token);
  if (!invite || invite.usedAt || invite.expiresAt.getTime() < Date.now()) redirect('/login?error=invite');
  const name = String(formData.get('name') || invite.name).trim();
  const password = String(formData.get('password') || '');
  const passwordHash = await bcrypt.hash(password, 10);
  const user = await prisma.user.upsert({
    where: { email: invite.email },
    update: { name, passwordHash, role: invite.role, active: true },
    create: { name, email: invite.email, passwordHash, role: invite.role, active: true },
  });
  await prisma.invite.update({ where: { token }, data: { usedAt: new Date() } });
  setSessionCookie(createSessionToken(user.id));
  redirect('/dashboard');
}

export default async function InvitePage({ params }: { params: Promise<{ token: string }> }) {
  const { token } = await params;
  const invite = await getInviteByToken(token);
  if (!invite || invite.usedAt || invite.expiresAt.getTime() < Date.now()) return notFound();
  return (
    <PageShell title="Accept your invite" description={`Create your login for ${invite.email}.`}>
      <div className="card mx-auto max-w-md p-6">
        <form action={acceptInviteAction.bind(null, token)} className="space-y-4">
          <div>
            <label className="mb-2 block text-sm font-medium text-slate-700">Name</label>
            <input className="input" name="name" defaultValue={invite.name} required />
          </div>
          <div>
            <label className="mb-2 block text-sm font-medium text-slate-700">Password</label>
            <input className="input" name="password" type="password" minLength={8} required />
          </div>
          <button className="button w-full" type="submit">Create account</button>
        </form>
      </div>
    </PageShell>
  );
}
