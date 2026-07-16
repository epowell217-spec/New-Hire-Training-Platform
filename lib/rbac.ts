import { Role } from './types';

export function canAdminister(role: Role) {
  return role === 'admin' || role === 'ceo';
}
