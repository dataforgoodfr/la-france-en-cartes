import type { Metadata } from "next";
import "./globals.css";


export const metadata: Metadata = {
  title: "La France à la loupe",
  description: "Une collaboration Data For Good et The Conversation",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="fr"
      className={`h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
