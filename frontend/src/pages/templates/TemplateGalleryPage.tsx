import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { templateService } from '../../services/templateService';

const CATEGORIES = ['All', 'Education', 'Business', 'Creative', 'Pitch Deck'];

export const TemplateGalleryPage = () => {
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [duplicateSuccess, setDuplicateSuccess] = useState<string | null>(null);

  const { data: templates = [], isLoading, error } = useQuery({
    queryKey: ['templates', selectedCategory],
    queryFn: () => templateService.getPublicTemplates(selectedCategory === 'All' ? undefined : selectedCategory)
  });

  const handleDuplicate = async (templateId: string, title: string) => {
    try {
      await templateService.duplicateTemplate(templateId);
      setDuplicateSuccess(`Successfully duplicated "${title}" to your presentations!`);
      setTimeout(() => setDuplicateSuccess(null), 3000);
    } catch (err) {
      alert('Failed to duplicate template');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Template Gallery</h2>
      </div>

      {duplicateSuccess && (
        <div className="bg-green-50 text-green-800 p-4 rounded-md">
          {duplicateSuccess}
        </div>
      )}

      <div className="flex space-x-2 overflow-x-auto pb-2">
        {CATEGORIES.map(category => (
          <button
            key={category}
            onClick={() => setSelectedCategory(category)}
            className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap ${
              selectedCategory === category
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
            }`}
          >
            {category}
          </button>
        ))}
      </div>

      {isLoading ? (
        <div>Loading templates...</div>
      ) : error ? (
        <div className="text-red-600">Failed to load templates.</div>
      ) : templates.length === 0 ? (
        <div className="text-gray-500 py-10 text-center">No templates found in this category.</div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {templates.map((template: any) => (
            <div key={template.id} className="bg-white rounded-lg shadow overflow-hidden flex flex-col">
              <div className="h-48 bg-gray-200 w-full relative">
                {template.thumbnail_url ? (
                  <img src={template.thumbnail_url} alt={template.title} className="w-full h-full object-cover" />
                ) : (
                  <div className="flex items-center justify-center w-full h-full text-gray-400">No Preview</div>
                )}
                <span className="absolute top-2 right-2 bg-white/90 px-2 py-1 text-xs font-semibold rounded text-gray-700 shadow-sm">
                  {template.category || 'General'}
                </span>
              </div>
              <div className="p-4 flex-1 flex flex-col">
                <h3 className="font-semibold text-lg text-gray-900 line-clamp-1">{template.title}</h3>
                <p className="text-sm text-gray-500 mt-1 line-clamp-2 flex-1">
                  {template.description || 'No description provided.'}
                </p>
                <button
                  onClick={() => handleDuplicate(template.id, template.title)}
                  className="mt-4 w-full bg-indigo-50 text-indigo-700 hover:bg-indigo-100 py-2 rounded font-medium transition-colors"
                >
                  Duplicate to My Presentations
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
