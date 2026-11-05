import Navbar from "@/components/Navbar";

export default function PageTemplate({ title, slug }: Props) {
  return (
    <main>
      <Navbar />
      <h1>{title}</h1>
      <p>
        Lorem ipsum...
      </p>
      <iframe
        src={`/${slug}/dataviz`}
        title="{title}"
        allow-scripts="true"
        allow="fullscreen *"
        style={{ border: 0, width: "100vw", height: "50vh" }}
      />
    </main>
  );
}
