import crypto from 'crypto';
import { cookies } from 'next/headers';
import { prisma } from './db';
import type { User } from './types';

const COOKIE_NAME = 'cfl_session';
const SESSION_SECRET = process.env.SESSION_SECRET || 'dev-session-secret-change-me';

function sign(value: string) {
  return crypto.createHmac('sha256', SESSION_SECRET).update(value).digest('base64url');
}

export function createSessionToken(userId: string) {
  const encoded = Buffer.from(JSON.stringify({ userId, iat: Date.now() })).toString('base64url');
  return `${encoded}.${sign(encoded)}`;
}

export function verifySessionToken(token: string) {
  const [encoded, signature] = token.split('.');
  if (!encoded || !signature) return null;
  const expected = sign(encoded);
  if (signature.length !== expected.length) return null;
  if (!crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expected))) return null;
  try {
    const payload = JSON.parse(Buffer.from(encoded, 'base64url').toString('utf8')) as { userId?: string };
    return typeof payload.userId === 'string' ? payload.userId : null;
  } catch {
    return null;
  }
}

export async function getCurrentUser(): Promise<User | null> {
  const token = cookies().get(COOKIE_NAME)?.value;
  if (!token) return null;
  const userId = verifySessionToken(token);
  if (!userId) return null;
  const user = await prisma.user.findUnique({ where: { id: userId } });
  if (!user || !user.active) return null;
  return { id: user.id, name: user.name, email: user.email, role: user.role, active: user.active };
}

export function setSessionCookie(token: string) {
  cookies().set(COOKIE_NAME, token, { httpOnly: true, sameSite: 'lax', secure: process.env.NODE_ENV === 'production', path: '/' });
}

export function clearSessionCookie() {
  cookies().delete(COOKIE_NAME);
}
