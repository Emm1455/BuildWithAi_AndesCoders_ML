FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

# Set environment variables for Supabase (uncomment and set your values for local dev)
# ENV SUPABASE_URL=your_supabase_url
# ENV SUPABASE_KEY=your_supabase_key

RUN python train.py

EXPOSE 8080
CMD ["python", "main.py"]