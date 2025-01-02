'use client';

import { useState, useCallback } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { AlertCircle } from "lucide-react";
import { CloudArrowUpIcon } from '@heroicons/react/24/outline';

interface Analysis {
  key_financial_metrics: string[];
  risks_and_challenges: string[];
  strategic_initiatives: string[];
  significant_changes: string[];
}

export default function FileUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile?.type === 'application/pdf') {
      setFile(droppedFile);
      setError(null);
    } else {
      setError('Please upload a PDF file');
    }
  }, []);

  const handleSubmit = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await axios.post<Analysis>(`${apiUrl}/analyze`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setAnalysis(response.data);
    } catch (err) {
      setError('Error analyzing the document. Please try again.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const categories = {
    'Key Financial Metrics': 'Learn about the company\'s financial performance',
    'Risks and Challenges': 'Understand potential threats and obstacles',
    'Strategic Initiatives': 'Discover future plans and strategies',
    'Significant Changes': 'Track important company developments'
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-gray-50 p-4 md:p-8">
      {/* Rest of your component code stays the same */}
      <div className="max-w-3xl mx-auto space-y-8">
        <div className="text-center space-y-2">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900">
            10-K Filing Analyzer
          </h1>
          <p className="text-gray-600">
            Upload your 10-K PDF file for instant AI-powered insights
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Upload Document</CardTitle>
          </CardHeader>
          <CardContent>
            <div
              onDrop={onDrop}
              onDragOver={(e) => e.preventDefault()}
              className="border-2 border-dashed border-gray-200 rounded-lg p-8 text-center transition-colors hover:border-blue-400 cursor-pointer bg-gray-50"
            >
              <CloudArrowUpIcon className="mx-auto h-12 w-12 text-gray-400" />
              <div className="mt-4">
                <label className="cursor-pointer">
                  <span className="text-sm text-gray-600">
                    Drop your file here, or{' '}
                    <span className="text-blue-600 hover:text-blue-500">browse</span>
                  </span>
                  <input
                    type="file"
                    className="hidden"
                    accept=".pdf"
                    onChange={(e) => {
                      const selectedFile = e.target.files?.[0];
                      if (selectedFile) setFile(selectedFile);
                    }}
                  />
                </label>
                <p className="mt-1 text-xs text-gray-500">PDF up to 10MB</p>
              </div>
            </div>

            {file && (
              <div className="mt-4">
                <div className="flex items-center justify-between bg-gray-50 px-4 py-3 rounded-md">
                  <span className="text-sm text-gray-600 truncate">{file.name}</span>
                  <button
                    onClick={handleSubmit}
                    disabled={loading}
                    className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                  >
                    {loading ? 'Analyzing...' : 'Analyze Document'}
                  </button>
                </div>
              </div>
            )}

            {error && (
              <Alert variant="destructive" className="mt-4">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}
          </CardContent>
        </Card>

        {analysis && (
          <div className="space-y-6">
            {Object.entries(analysis).map(([category, items]) => (
              <Card key={category}>
                <CardHeader>
                  <CardTitle>
                    {category.split('_').map(word => 
                      word.charAt(0).toUpperCase() + word.slice(1)
                    ).join(' ')}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {items.map((item, index) => (
                      <li key={index} className="text-sm text-gray-700 leading-relaxed">
                        {item}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {!analysis && (
          <div className="grid md:grid-cols-2 gap-4 mt-8">
            {Object.entries(categories).map(([title, description]) => (
              <Card key={title}>
                <CardHeader>
                  <CardTitle className="text-lg">{title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600">{description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}