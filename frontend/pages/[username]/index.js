/* eslint-disable react/prop-types */
import { getUserWithUsername } from '@lib/firebase';
import UserProfile from '@components/UserProfile';
import Metatags from '@components/Metatags';

export async function getServerSideProps({ query }) {
  const { username } = query;

  const userDoc = await getUserWithUsername(username);

  // If no user, short circuit to 404 page
  if (!userDoc) {
    return {
      notFound: true,
    };
  }

  // JSON serializable data
  let user = null;

  if (userDoc) {
    user = userDoc.data();
  }

  return {
    props: { user },
  };
}

export default function UserProfilePage({ user }) {
  return (
    <main>
      <Metatags title={user.username} description={`${user.username}'s public profile`} />
      <UserProfile user={user} />
    </main>
  );
}
