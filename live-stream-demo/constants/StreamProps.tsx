export interface Chapter {
    timestamp: string;
    description: string;
  }
  
  export interface ScheduledStreamProps {
    streamer_name: string;
    video_url: string;
    stream_title: string;
    stream_description?: string;
    start_time: string;
    end_time: string;
    tags: string[];
    chapters: Chapter[];
  }