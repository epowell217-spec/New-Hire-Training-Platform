import { demoUsers } from './data';
import { User } from './types';

export async function getCurrentUser(): Promise<User> {
  return demoUsers[0];
}
