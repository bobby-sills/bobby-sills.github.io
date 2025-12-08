export interface Post {
  slug: string;
  title: string;
  date: string;
  tags: string[];
  image?: string;
  html: string;
}

// Import all markdown files from the posts directory
const modules = import.meta.glob('/posts/*.md', { eager: true });

export function getAllPosts(): Post[] {
  const posts: Post[] = [];

  for (const path in modules) {
    const module = modules[path] as any;
    const slug = path.split('/').pop()?.replace('.md', '') || '';

    posts.push({
      slug,
      title: module.attributes?.title || 'Untitled',
      date: module.attributes?.date || '',
      tags: module.attributes?.tags || [],
      image: module.attributes?.image,
      html: module.html || ''
    });
  }

  // Sort by date, newest first
  return posts.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
}

export function getPostBySlug(slug: string): Post | undefined {
  return getAllPosts().find(post => post.slug === slug);
}
