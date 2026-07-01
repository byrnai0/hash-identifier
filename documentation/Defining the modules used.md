___

# 1. **Regex basics: Python** **re** **module**

The Python `re` module provides regular expression matching operations. Here is a breakdown of the three functions you asked about:

- **re.compile(pattern, flags=0)**: This function compiles a regular expression pattern into a regular expression object. This compiled object can then be reused for matching operations (like `match()` and `search()`). Saving and reusing a compiled regular expression object is highly recommended for efficiency if the expression will be used several times within a single program.

- **re.match(pattern, string, flags=0)**: This function checks if zero or more characters at the **beginning** of a string match the regular expression pattern. If there is a match, it returns a `Match` object; if not, it returns `None`. It is important to note that even if `MULTILINE` mode is enabled, `re.match()` will only look at the very beginning of the string, not at the beginning of each individual line.

- **re.fullmatch(pattern, string, flags=0)**: This function checks if the **entire** string matches the regular expression pattern. It returns a `Match` object only if the whole string is a match, and returns `None` otherwise

# 2. **hashID on PyPI (Handling 220+ types)**

According to the PyPI documentation, hashID identifies over 220 unique hash types by utilizing **regular expressions**. It works by matching the input against these regular expressions to determine the encryption type. It is capable of identifying a single hash from standard input, parsing a single file, or reading multiple files within a directory to identify the hashes inside them. Additionally, hashID can output the corresponding Hashcat mode and/or JohnTheRipper formats for the identified hashes.

# 3. Rich library's classes

**-> Console Protocol** Rich uses a Console Protocol to add rich formatting capabilities to custom objects, allowing them to be printed with styles, colors, and formatting. You can customize how your objects are rendered by implementing specific methods:

- **__rich__** **method:** This is the simplest way to customize output. It returns a single object that Rich knows how to render, such as Text or a Table.
- **__rich_console__** **method:** For more advanced rendering, this method accepts a **Console** and a `ConsoleOptions` instance and yields an iterable of renderable objects. For total control, it can yield low-level `Segment` objects, which consist of text and an optional style.
- **__rich_measure__** **method:** Sometimes Rich needs to know an object's dimensions (like when calculating column sizes for a Table). This method accepts a `Console` and `ConsoleOptions` and returns a `Measurement` object containing the minimum and maximum character width required to render the object.

**-> Panel** The **Panel** class is used to **draw a border around text or other renderables**.

- You construct it by passing your renderable as the first positional argument.
- By default, panels extend to the full width of the terminal, but you can force the panel to fit its content tightly by setting `expand=False` in the constructor or by using `fit()`.
- Panels are highly customizable: you can change the border style with the `box` argument, and you can easily add a `title` (top border) and `subtitle` (bottom border).

**-> Table** The **Table** class offers robust tools to render tabular data.

- You create a table by constructing a `Table` object, defining columns with **add_column()**, and adding data with **add_row()**. A row is not limited to text; it can contain any renderable Rich object, including another table.
- Rich automatically **calculates optimal column sizes** to fit your content and will wrap text if the terminal isn't wide enough.
- There are extensive styling options available in the constructor, such as zebra striping (`row_styles`), adding lines between all rows (`show_lines=True`), modifying border styles (`box`), and setting custom padding.
- The `Table` class can also function as a **layout tool**. By using the alternative `grid()` constructor, it disables borders and headers, allowing you to use the table grid to easily align and position text across the terminal.