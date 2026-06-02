import { useAuthStore } from '../store/authStore';

const getHeaders = () => {
  const token = useAuthStore.getState().token;
  return {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {})
  };
};

export const templateService = {
  getPublicTemplates: async (category?: string) => {
    const url = category ? `/api/templates?category=${encodeURIComponent(category)}` : '/api/templates';
    const response = await fetch(url, { headers: getHeaders() });
    if (!response.ok) throw new Error('Failed to fetch templates');
    return response.json();
  },

  duplicateTemplate: async (templateId: string) => {
    const response = await fetch(`/api/templates/${templateId}/duplicate`, {
      method: 'POST',
      headers: getHeaders()
    });
    if (!response.ok) throw new Error('Failed to duplicate template');
    return response.json();
  }
};
