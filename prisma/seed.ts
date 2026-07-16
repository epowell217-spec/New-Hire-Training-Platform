import bcrypt from 'bcryptjs';
import { prisma } from '../lib/db';

async function main() {
  const passwordHash = await bcrypt.hash('ChangeMe123!', 10);

  await prisma.user.upsert({
    where: { email: 'ceo@example.org' },
    update: { passwordHash, active: true, role: 'ceo' },
    create: { name: 'CEO Demo', email: 'ceo@example.org', passwordHash, role: 'ceo', active: true },
  });

  await prisma.user.upsert({
    where: { email: 'admin@example.org' },
    update: { passwordHash, active: true, role: 'admin' },
    create: { name: 'Admin Demo', email: 'admin@example.org', passwordHash, role: 'admin', active: true },
  });

  await prisma.user.upsert({
    where: { email: 'newhire@example.org' },
    update: { passwordHash, active: true, role: 'employee' },
    create: { name: 'New Hire Demo', email: 'newhire@example.org', passwordHash, role: 'employee', active: true },
  });

  const modules = [
    { title: 'HIPAA Compliance', slug: 'hipaa-compliance', description: 'Protected health information, privacy basics, and reporting expectations.', videoUrl: 'https://videos.example.org/hipaa.mp4', order: 1 },
    { title: 'Resident Abuse and Neglect', slug: 'resident-abuse-neglect', description: 'Recognizing, reporting, and preventing abuse or neglect.', videoUrl: 'https://videos.example.org/abuse-neglect.mp4', order: 2 },
    { title: 'Hand Washing Safety', slug: 'hand-washing-safety', description: 'When to wash hands and proper infection control basics.', videoUrl: 'https://videos.example.org/handwashing.mp4', order: 3 },
    { title: 'Active Shooter Safety', slug: 'active-shooter-safety', description: 'Run, hide, fight guidance and facility response procedures.', videoUrl: 'https://videos.example.org/active-shooter.mp4', order: 4 },
  ];

  for (const module of modules) {
    await prisma.trainingModule.upsert({ where: { slug: module.slug }, update: module, create: module });
  }
}

main().finally(async () => { await prisma.$disconnect(); });
