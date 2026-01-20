from crewai.tools import BaseTool
import json
from typing import List, Dict
import re

class AnalysisTool(BaseTool):
    name: str = "Content Analysis Tool"
    description: str = (
        "Analyzes research content to extract key insights, identify patterns, "
        "and detect contradictions. Input should be JSON string containing "
        "multiple source contents to compare."
    )
    
    def _run(self, content: str) -> str:
        """
        Analyze research content for insights and contradictions
        """
        try:
            # Parse input
            if isinstance(content, str):
                try:
                    data = json.loads(content)
                except json.JSONDecodeError:
                    # Treat as single text content
                    data = {"sources": [{"content": content}]}
            else:
                data = content
            
            sources = data.get("sources", [])
            
            if not sources:
                return json.dumps({
                    "status": "error",
                    "message": "No sources provided for analysis"
                })
            
            # Extract key statistics
            total_word_count = 0
            all_keywords = []
            source_summaries = []
            
            for idx, source in enumerate(sources):
                text = source.get("content", "")
                words = text.split()
                total_word_count += len(words)
                
                # Extract potential keywords (simplified)
                # Look for capitalized words and repeated terms
                keywords = self._extract_keywords(text)
                all_keywords.extend(keywords)
                
                source_summaries.append({
                    "source_id": idx,
                    "url": source.get("url", "Unknown"),
                    "word_count": len(words),
                    "key_topics": keywords[:5]
                })
            
            # Find common themes
            keyword_freq = {}
            for kw in all_keywords:
                keyword_freq[kw] = keyword_freq.get(kw, 0) + 1
            
            common_themes = sorted(
                keyword_freq.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:10]
            
            # Detect potential contradictions (simplified heuristic)
            contradictions = self._detect_contradictions(sources)
            
            result = {
                "status": "success",
                "analysis": {
                    "total_sources": len(sources),
                    "total_word_count": total_word_count,
                    "common_themes": [{"theme": t[0], "frequency": t[1]} for t in common_themes],
                    "source_summaries": source_summaries,
                    "potential_contradictions": contradictions,
                    "recommendation": self._generate_recommendation(sources, contradictions)
                }
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Analysis failed: {str(e)}"
            })
    
    def _extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """Extract potential keywords from text"""
        # Remove common words and extract meaningful terms
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                       'of', 'with', 'is', 'was', 'are', 'were', 'been', 'be', 'have', 'has',
                       'that', 'this', 'it', 'from', 'by', 'as'}
        
        words = re.findall(r'\b[A-Z][a-z]+\b|\b[a-z]{4,}\b', text)
        keywords = [w.lower() for w in words if w.lower() not in common_words]
        
        # Count frequency
        freq = {}
        for kw in keywords:
            freq[kw] = freq.get(kw, 0) + 1
        
        return [k for k, v in sorted(freq.items(), key=lambda x: x[1], reverse=True)[:top_n]]
    
    def _detect_contradictions(self, sources: List[Dict]) -> List[Dict]:
        """Detect potential contradictions between sources"""
        contradictions = []
        
        # Simple heuristic: look for opposing terms
        opposing_pairs = [
            ('increase', 'decrease'),
            ('rise', 'fall'),
            ('growth', 'decline'),
            ('positive', 'negative'),
            ('improve', 'worsen'),
            ('success', 'failure'),
            ('gain', 'loss')
        ]
        
        for i, source1 in enumerate(sources):
            text1 = source1.get("content", "").lower()
            for j, source2 in enumerate(sources[i+1:], start=i+1):
                text2 = source2.get("content", "").lower()
                
                for term1, term2 in opposing_pairs:
                    if term1 in text1 and term2 in text2:
                        contradictions.append({
                            "source_1": source1.get("url", f"Source {i}"),
                            "source_2": source2.get("url", f"Source {j}"),
                            "type": f"Opposing terms: {term1} vs {term2}",
                            "severity": "medium"
                        })
        
        return contradictions[:5]  # Limit to top 5
    
    def _generate_recommendation(self, sources: List[Dict], contradictions: List[Dict]) -> str:
        """Generate analysis recommendation"""
        if len(contradictions) > 3:
            return "High variance detected. Additional fact-checking recommended."
        elif len(sources) < 3:
            return "Limited sources. Consider gathering more data for comprehensive analysis."
        else:
            return "Sources show good consistency. Proceed with synthesis."