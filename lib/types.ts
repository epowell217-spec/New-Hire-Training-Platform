export type Role = 'employee' | 'admin' | 'ceo';

export type User = {
  id: string;
  name: string;
  email: string;
  role: Role;
  active: boolean;
};

export type TrainingModule = {
  id: string;
  title: string;
  slug: string;
  description: string;
  videoUrl: string;
  order: number;
  required: boolean;
};
