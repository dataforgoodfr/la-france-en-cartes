"use client"

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/", text: "Accueil" },
  { href: "/immigration", text: "Immigration" },
  { href: "/education", text: "Éducation" },
  { href: "/sante", text: "Santé" },
  { href: "/agriculture", text: "Agriculture" },
  { href: "/securite", text: "Sécurité" },
  { href: "/mentions-legales", text: "Mentions légales" },
];

export default function Navbar() {
  const pathname = usePathname();

  return (
    <nav className="flex gap-4">
      {links.map((link) => {
        let isActive;

        if (link.href === "/") {
          isActive = pathname === link.href;
        } else {
          isActive = pathname.startsWith(link.href);
        }

        return (
          <Link key={link.href} href={link.href} className={isActive ? "highlight" : "" } >{link.text}</Link>
        );
      })}
    </nav>
  );
}
