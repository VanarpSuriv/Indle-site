// Shared only by this page and its tests. No credentials or user IDs are logged.
export async function deleteVerifiedAccount(user, services) {
  if (!user?.uid) throw new Error('SIGN_IN_REQUIRED');
  const uid = user.uid;
  await services.reauthenticate(user);
  if (user.uid !== uid) throw new Error('IDENTITY_CHANGED');
  const token = await user.getIdToken(true);
  const result = await services.deleteCloud(token);
  if (result?.deleted !== true) throw new Error('CLOUD_DELETION_NOT_CONFIRMED');
  try {
    await services.deleteIdentity(user);
  } catch {
    throw new Error('IDENTITY_DELETION_INCOMPLETE');
  }
  await services.clearSession();
}
