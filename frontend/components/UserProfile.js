/* eslint-disable jsx-a11y/alt-text */
/* eslint-disable react/prop-types */
// UI component for user profile
export default function UserProfile({ user }) {
  return (
    <div className="box-center">
      <img src={user.photoURL || '/user.png'} className="card-img-center" />
      <p>
        <i>
          @
          {user.username}
        </i>
      </p>
      <h1>{user.displayName || 'Anonymous User'}</h1>
    </div>
  );
}
