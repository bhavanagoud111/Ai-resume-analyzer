import { render, screen } from '@testing-library/react';
import App from './App';

// axios ships as an ES module that the Create React App Jest setup does not
// transform, and the test should not make network requests anyway.
jest.mock('axios', () => ({
  __esModule: true,
  default: { post: jest.fn() },
}));

test('renders the resume form', () => {
  render(<App />);
  expect(screen.getByText(/resume analyzer/i)).toBeInTheDocument();
  expect(screen.getByPlaceholderText(/paste your resume here/i)).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /analyze/i })).toBeInTheDocument();
});
