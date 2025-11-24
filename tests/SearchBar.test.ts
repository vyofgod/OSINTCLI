import { render, fireEvent } from '@testing-library/svelte';
import SearchBar from '../src/components/SearchBar.svelte';

const suggestions = [
  { term: 'hydra', at: new Date().toISOString() },
  { term: 'umbra', at: new Date().toISOString() }
];

describe('SearchBar', () => {
  test('validates email and phone rules', async () => {
    const { getByLabelText, findByRole } = render(SearchBar, { props: { suggestions } });
    const input = getByLabelText('UmbraTrace search') as HTMLInputElement;
    await fireEvent.input(input, { target: { value: 'invalid@' } });
    await fireEvent.keyDown(input, { key: 'Enter', code: 'Enter' });
    expect(await findByRole('alert')).toHaveTextContent('valid email');
  });

  test('emits search on enter', async () => {
    const { getByLabelText, component } = render(SearchBar, { props: { suggestions } });
    const input = getByLabelText('UmbraTrace search') as HTMLInputElement;
    const fn = vi.fn();
    component.$on('search', fn);
    await fireEvent.input(input, { target: { value: 'hydra@example.com' } });
    await fireEvent.keyDown(input, { key: 'Enter', code: 'Enter' });
    expect(fn).toHaveBeenCalled();
  });

  test('shows suggestion dropdown', () => {
    const { getByText } = render(SearchBar, { props: { suggestions } });
    expect(getByText('Recent')).toBeInTheDocument();
  });
});
