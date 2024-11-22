import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="bg-dark p-4">
      <div className="container mx-auto flex justify-between items-center">
        <div className="flex space-x-4">
          <Link href="/" className="text-decoration-none">
            <span className="text-light fw-semibold">Home</span>
          </Link>
          <Link href="/me" className="text-decoration-none">
            <span className="text-light fw-semibold">Profile</span>
          </Link>
          <Link href="/tournament" className="text-decoration-none">
            <span className="text-light fw-semibold">Tournament</span>
          </Link>
          <Link href="/lobby" className="text-decoration-none">
            <span className="text-light fw-semibold">Lobby</span>
          </Link>
        </div>
      </div>
    </nav>
  );
}
