# API Documentation

## Base URL

```
Development: http://localhost:8000/api/v1
Production: https://your-domain.com/api/v1
```

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```bash
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Carousels

#### POST /carousels/generate

Generate a new carousel.

**Request:**
```json
{
  "topic": "How vector embeddings work in AI",
  "carousel_type": "explainer",
  "slide_count": 8,
  "target_audience": "AI developers",
  "brand_voice": "educational_engaging",
  "auto_publish": false,
  "generate_variants": true
}
```

**Response (202 Accepted):**
```json
{
  "carousel_id": "uuid",
  "status": "queued",
  "message": "Carousel generation started",
  "estimated_time_minutes": 8
}
```

#### GET /carousels/

List user's carousels with pagination.

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `page_size` (int): Results per page (default: 20)
- `status_filter` (string): Filter by status

**Response:**
```json
{
  "carousels": [...],
  "total": 42,
  "page": 1,
  "page_size": 20
}
```

#### GET /carousels/{carousel_id}

Get carousel details including all slides.

**Response:**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "topic": "...",
  "status": "completed",
  "slide_count": 8,
  "caption": "...",
  "hashtags": ["ai", "machinelearning"],
  "total_cost": 2.85,
  "slides": [...]
}
```

#### GET /carousels/{carousel_id}/progress

Get real-time generation progress.

**Response:**
```json
{
  "carousel_id": "uuid",
  "status": "designing",
  "progress_percentage": 75,
  "current_step": "Generating visuals",
  "estimated_time_remaining_minutes": 2
}
```

### Research

#### POST /research/topic

Research a topic before carousel generation.

**Request:**
```json
{
  "topic": "GPT-4 Vision API",
  "include_reddit": true,
  "include_twitter": true,
  "timeframe": "7d"
}
```

**Response:**
```json
{
  "topic": "GPT-4 Vision API",
  "sources": ["perplexity", "reddit", "twitter"],
  "key_facts": [...],
  "visual_opportunities": [...],
  "trending_discussions": [...],
  "validation_score": 8.5,
  "estimated_engagement": {...}
}
```

### Analytics

#### GET /analytics/{carousel_id}

Get performance metrics for a published carousel.

**Response:**
```json
{
  "carousel_id": "uuid",
  "impressions": 3450,
  "reach": 2890,
  "likes": 287,
  "comments": 45,
  "saves": 312,
  "shares": 67,
  "engagement_rate": 12.5,
  "save_rate": 9.0
}
```

#### GET /analytics/{carousel_id}/prediction

Predict performance before publishing.

**Response:**
```json
{
  "predicted_impressions": {"min": 2000, "max": 4000},
  "predicted_saves": {"min": 150, "max": 350},
  "confidence_score": 0.78,
  "optimal_posting_time": "2025-10-10T19:00:00Z"
}
```

### Publishing

#### POST /publishing/publish

Publish carousel to Instagram.

**Request:**
```json
{
  "carousel_id": "uuid",
  "publish_immediately": true,
  "caption_override": "Optional custom caption"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Carousel published successfully"
}
```

### Trending

#### GET /trending/

Get trending AI topics.

**Query Parameters:**
- `timeframe` (string): "7d" or "30d"
- `limit` (int): Number of topics (default: 10)

**Response:**
```json
{
  "topics": [
    {
      "topic": "Claude 3.5 Sonnet features",
      "trend_score": 9.2,
      "sources": ["reddit", "twitter"],
      "discussion_count": 342
    }
  ],
  "timeframe": "7d",
  "generated_at": "2025-10-09T12:00:00Z"
}
```

## Error Responses

All errors follow this format:

```json
{
  "error": "Error message",
  "details": {
    "field": "Additional error details"
  },
  "timestamp": "2025-10-09T12:00:00Z"
}
```

### Common HTTP Status Codes

- `200` - Success
- `201` - Created
- `202` - Accepted (async operation started)
- `204` - No Content
- `400` - Bad Request (validation error)
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Unprocessable Entity
- `429` - Too Many Requests
- `500` - Internal Server Error
- `503` - Service Unavailable

## Rate Limits

- Carousel generation: 100 per day per user
- API requests: 60 per minute per user
- Research: 50 per hour per user

Headers included in responses:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1633024800
```

## Webhooks

Configure webhooks for carousel completion:

```bash
POST /webhooks/carousel-complete
```

**Payload:**
```json
{
  "carousel_id": "uuid",
  "status": "completed",
  "total_cost": 2.85,
  "timestamp": "2025-10-09T12:00:00Z"
}
```

## Interactive API Documentation

Visit http://localhost:8000/docs for interactive Swagger UI documentation.
