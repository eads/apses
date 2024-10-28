import fs from 'fs';
import path from 'path';
import { remark } from 'remark';
import remarkRehype from 'remark-rehype';
import rehypeStringify from 'rehype-stringify';

export async function load({ params, fetch }) {
  const { state_slug: slug } = params;

  // Load and preprocess Markdown file
  const filePath = path.join('src', 'summaries', `${slug}_description.md`);
  let description = null;

  try {
    let fileContent = fs.readFileSync(filePath, 'utf-8');

    // Split lines and filter out the first two lines
    let lines = fileContent.split('\n').slice(2);

    // Truncate at the first occurrence of "### Math"
    const mathIndex = lines.findIndex(line => line.includes('### Math'));
    if (mathIndex !== -1) {
      lines = lines.slice(0, mathIndex);
    }

    // Join the remaining lines back together
    fileContent = lines.join('\n');

    // Process the truncated content with Remark
    const parsedContent = await remark()
      .use(remarkRehype)
      .use(rehypeStringify)
      .process(fileContent);
    description = parsedContent.toString();
  } catch (err) {
    description = null;
  }

  // Load JSON data
  const response = await fetch(`/files/${slug}_data.json`);
  const rawData = await response.json();
  const stateData = rawData
    .filter(d => d.year > 2003)
    .map(d => ({
      ...d,
      ft_pay_per_ft_employee: d.ft_pay / d.ft_employment,
      pt_pay_per_pt_employee: d.pt_pay / d.pt_employment,
    }));

  return {
    description,
    stateData,
    stateSlug: slug,
  };
}
