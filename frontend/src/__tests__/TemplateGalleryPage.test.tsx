import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { TemplateGalleryPage } from '../pages/templates/TemplateGalleryPage';
import { vi } from 'vitest';
import * as templateServiceModule from '../services/templateService';

// Properly mock the module
vi.spyOn(templateServiceModule.templateService, 'getPublicTemplates').mockResolvedValue([
  { id: '1', title: 'Business Pitch', category: 'Business', description: 'A pitch deck', thumbnail_url: null },
  { id: '2', title: 'Science Lesson', category: 'Education', description: 'For teachers', thumbnail_url: null }
]);
vi.spyOn(templateServiceModule.templateService, 'duplicateTemplate').mockResolvedValue({ id: 'new_1', title: 'Copy of Business Pitch' });

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: false } }
});

describe('TemplateGalleryPage', () => {
  it('renders templates and handles category switching', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <TemplateGalleryPage />
      </QueryClientProvider>
    );

    // Check loading state (briefly)
    expect(screen.getByText(/Template Gallery/i)).toBeInTheDocument();

    // Wait for templates to load
    await waitFor(() => {
        expect(screen.getByText('Business Pitch')).toBeInTheDocument();
    });

    expect(screen.getByText('Science Lesson')).toBeInTheDocument();

    // Check categories
    const businessBtn = screen.getByText('Business', { selector: 'button' });
    fireEvent.click(businessBtn);

    expect(businessBtn.className).toContain('bg-indigo-600');
  });
});
