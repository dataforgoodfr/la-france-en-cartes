import Link from "next/link";

export default function Navbar() {
  return (
    <nav>
      <ul class="flex gap-4">
        <li>
          <Link href="/">Accueil</Link>
        </li>
        <li>
          <Link href="/immigration">Immigration</Link>
        </li>
        <li>
          <Link href="/education">Éducation</Link>
        </li>
        <li>
          <Link href="/sante">Santé</Link>
        </li>
        <li>
          <Link href="/agriculture">Agriculture</Link>
        </li>
        <li>
          <Link href="/securite">Sécurité</Link>
        </li>
        <li>
          <Link href="/mentions-legales">Mentions légales</Link>
        </li>
      </ul>
    </nav>
  );
}
