import crypto from 'crypto';
import { prisma } from './db';
import { Role } from './types';

export async function createInvite(input: { name: string; email: string; role: Role; createdById?: string }) {
  const token = crypto.randomBytes(24).toString('hex');
  return prisma.invite.create({
    data: {
      token,
      name: input.name,
      email: input.email,
      role: input.role,
      createdById: input.createdById,
      expiresAt: new Date(Date.now() + 1000 * 60 * 60 * 24 * 7),
    },
  });
}

export async function getInviteByToken(token: string) {
  return prisma.invite.findUnique({ where: { token } });
}
