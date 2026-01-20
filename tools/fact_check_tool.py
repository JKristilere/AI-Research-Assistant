from crewai.tools import BaseTool
import json
import re
from typing import List, Dict

class FactCheckTool(BaseTool):
    name: str = "Fact Verification Tool"
    description: str = (
        "Verifies claims against provided sources and checks for consistency. "
        "Input should be JSON with 'claims' and 'sources' fields."
    )
    
    def _run(self, input_data: str) -> str:
        """
        Verify claims against source material
        """
        try:
            # Parse input
            if isinstance(input_data, str):
                try:
                    data = json.loads(input_data)
                except json.JSONDecodeError:
                    return json.dumps({
                        "status": "error",
                        "message": "Invalid JSON input. Expected format: {claims: [...], sources: [...]}"
                    })
            else:
                data = input_data
            
            claims = data.get("claims", [])
            sources = data.get("sources", [])
            
            if not claims:
                return json.dumps({
                    "status": "error",
                    "message": "No claims provided for verification"
                })
            
            if not sources:
                return json.dumps({
                    "status": "error",
                    "message": "No sources provided for verification"
                })
            
            # Combine all source content
            all_source_text = " ".join([
                source.get("content", "") for source in sources
            ]).lower()
            
            verification_results = []
            
            for claim in claims:
                result = self._verify_claim(claim, all_source_text, sources)
                verification_results.append(result)
            
            # Calculate overall credibility score
            verified_count = sum(1 for r in verification_results if r["status"] == "verified")
            credibility_score = (verified_count / len(claims)) * 100 if claims else 0
            
            return json.dumps({
                "status": "success",
                "verification_results": verification_results,
                "summary": {
                    "total_claims": len(claims),
                    "verified": verified_count,
                    "unverified": len(claims) - verified_count,
                    "credibility_score": round(credibility_score, 2)
                }
            }, indent=2)
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Fact-checking failed: {str(e)}"
            })
    
    def _verify_claim(self, claim: str, source_text: str, sources: List[Dict]) -> Dict:
        """
        Verify a single claim against sources
        """
        claim_lower = claim.lower()
        
        # Extract key terms from claim (simple approach)
        key_terms = self._extract_key_terms(claim)
        
        # Check if key terms are present in sources
        matching_terms = []
        for term in key_terms:
            if term.lower() in source_text:
                matching_terms.append(term)
        
        match_percentage = (len(matching_terms) / len(key_terms) * 100) if key_terms else 0
        
        # Find supporting sources
        supporting_sources = []
        for source in sources:
            source_content = source.get("content", "").lower()
            if any(term.lower() in source_content for term in key_terms):
                supporting_sources.append({
                    "url": source.get("url", "Unknown"),
                    "title": source.get("title", "Untitled")
                })
        
        # Determine verification status
        if match_percentage >= 70:
            status = "verified"
            confidence = "high"
        elif match_percentage >= 40:
            status = "partially_verified"
            confidence = "medium"
        else:
            status = "unverified"
            confidence = "low"
        
        return {
            "claim": claim,
            "status": status,
            "confidence": confidence,
            "match_percentage": round(match_percentage, 2),
            "supporting_sources": supporting_sources[:3],
            "key_terms_found": matching_terms
        }
    
    def _extract_key_terms(self, text: str) -> List[str]:
        """Extract key terms from claim"""
        # Remove common words
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 
                       'for', 'of', 'with', 'is', 'was', 'are', 'were', 'been', 'be',
                       'has', 'have', 'had', 'that', 'this', 'it', 'from', 'by'}
        
        # Extract words (3+ characters)
        words = re.findall(r'\b\w{3,}\b', text.lower())
        key_terms = [w for w in words if w not in common_words]
        
        return key_terms[:10]  # Limit to top 10 terms