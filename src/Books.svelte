<script lang="ts">
  import Book from "./lib/Book.svelte";
  import Nav from "./lib/Nav.svelte";
  import ContributionGraph from "./lib/ContributionGraph.svelte";
  import koreaderBooks from "../data/koreader-books.json";
  import manualData from "../data/manual-data.json";

  $effect(() => {
    document.title = "books | bobby sills";
  });

  interface Book {
    title: string;
    authors: string;
    percentage_completed: number;
    total_pages?: number;
    date_completed?: string;
  }

  interface ManualBook {
    title: string;
    authors: string;
    status: "currently_reading" | "completed" | "want_to_read";
    total_pages?: number;
    pages_read?: number;
    date_completed?: string;
  }

  // Manual data is the source of truth for status
  // KOReader provides progress updates but doesn't override manual status
  const allBooks: Book[] = (manualData.books as ManualBook[])
    .filter((book) => book.status === "currently_reading" || book.status === "completed")
    .map((manualBook) => {
      // Try to find matching KOReader data for this book
      const koreaderBook = koreaderBooks.books.find(
        (kb) => kb.title === manualBook.title
      );

      // If manual status is "completed", keep it completed regardless of KOReader
      if (manualBook.status === "completed") {
        return {
          title: manualBook.title,
          authors: manualBook.authors,
          percentage_completed: 100,
          date_completed: manualBook.date_completed,
          total_pages: manualBook.total_pages,
        };
      }

      // For "currently_reading", prefer KOReader progress if available
      if (koreaderBook) {
        return {
          title: manualBook.title,
          authors: manualBook.authors,
          percentage_completed: koreaderBook.percentage_completed,
          total_pages: manualBook.total_pages,
          date_completed: koreaderBook.date_completed,
        };
      }

      // Fall back to manual data calculation
      return {
        title: manualBook.title,
        authors: manualBook.authors,
        percentage_completed: manualBook.pages_read && manualBook.total_pages
          ? (manualBook.pages_read / manualBook.total_pages) * 100
          : 0,
        total_pages: manualBook.total_pages,
      };
    });

  // Add want to read books from manual data
  const wantToRead = (manualData.books as ManualBook[])
    .filter((book) => book.status === "want_to_read")
    .map((book) => ({
      title: book.title,
      authors: book.authors,
    }));

  // Separate books into currently reading and completed
  const currentlyReading = allBooks.filter(
    (book) => book.percentage_completed < 100,
  );
  const completedBooks = allBooks.filter(
    (book) => book.percentage_completed >= 100,
  );
</script>

<main>
  <Nav />

  <h1>books</h1>

  <ContributionGraph />

  <h2>currently reading</h2>
  {#each currentlyReading as book (book.title)}
    <Book
      title={book.title}
      author={book.authors}
      percent={book.percentage_completed}
      totalPages={book.total_pages ?? 0}
    />
  {/each}

  <h2>completed</h2>
  {#each completedBooks as book (book.title)}
    <Book
      title={book.title}
      author={book.authors}
      percent={book.percentage_completed}
      totalPages={book.total_pages ?? 0}
      dateCompleted={book.date_completed}
    />
  {/each}

  <h2>up next</h2>
  {#each wantToRead as book (book.title)}
    <div
      style="display: flex; flex-direction: column; gap: 5px; margin-bottom: 20px;"
    >
      <span style="color: var(--fg); font-size: larger;">{book.title}</span>
      <span style="color: var(--fg4);">by {book.authors}</span>
    </div>
  {/each}
</main>

<style>
</style>
