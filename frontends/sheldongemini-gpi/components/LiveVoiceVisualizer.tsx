
import React, { useEffect, useRef } from 'react';

interface LiveVoiceVisualizerProps {
  isActive: boolean;
  isSpeaking: boolean; // Is the model speaking?
}

const LiveVoiceVisualizer: React.FC<LiveVoiceVisualizerProps> = ({ isActive, isSpeaking }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const requestRef = useRef<number>(0);
  const timeRef = useRef<number>(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const animate = () => {
      if (!isActive) {
          ctx.clearRect(0, 0, canvas.width, canvas.height);
          return;
      }

      timeRef.current += 0.05;
      const t = timeRef.current;
      
      // Resize handling
      if (canvas.width !== canvas.clientWidth || canvas.height !== canvas.clientHeight) {
        canvas.width = canvas.clientWidth;
        canvas.height = canvas.clientHeight;
      }

      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const w = canvas.width;
      const h = canvas.height;
      const cy = h / 2;

      // Base line logic
      ctx.lineWidth = 2;
      
      const lines = 3;
      
      for (let i = 0; i < lines; i++) {
          ctx.beginPath();
          
          // Color based on state
          if (isSpeaking) {
              // Active speaking: Cyan/Blue energetic
              ctx.strokeStyle = `rgba(6, 182, 212, ${0.5 + Math.sin(t + i) * 0.2})`; // Cyan-500
          } else {
              // Listening/Idle: Amber/Orange waiting
              ctx.strokeStyle = `rgba(245, 158, 11, ${0.3 + Math.sin(t * 0.5 + i) * 0.1})`; // Amber-500
          }

          for (let x = 0; x < w; x += 5) {
              const normalizedX = x / w;
              
              // Waveform math
              // Base wave
              let y = Math.sin(normalizedX * 10 + t + i) * 20;
              
              // Modulation (make it look like voice or breathing)
              const amplitude = isSpeaking ? 40 : 10;
              const frequency = isSpeaking ? 15 : 2;
              
              // Add complexity
              y += Math.sin(normalizedX * frequency + t * 2) * amplitude * Math.sin(normalizedX * Math.PI); // Envelope

              ctx.lineTo(x, cy + y);
          }
          ctx.stroke();
      }

      requestRef.current = requestAnimationFrame(animate);
    };

    requestRef.current = requestAnimationFrame(animate);

    return () => cancelAnimationFrame(requestRef.current);
  }, [isActive, isSpeaking]);

  return <canvas ref={canvasRef} className="w-full h-32 md:h-48 rounded-lg bg-gray-900/50 backdrop-blur-sm border border-gray-700 shadow-inner" />;
};

export default LiveVoiceVisualizer;
