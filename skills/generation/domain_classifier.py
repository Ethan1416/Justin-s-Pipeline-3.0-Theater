"""
Domain Classifier - Classify content into NCLEX domains for the pipeline.

This module classifies anchor content into the 6 NCLEX content domains:
1. Fundamentals of Nursing
2. Pharmacology
3. Medical-Surgical Nursing
4. OB/Maternity Nursing
5. Pediatric Nursing
6. Mental Health Nursing

Used in Step 3 (Official Sorting) of the preparation pipeline.

Usage:
    from skills.generation.domain_classifier import DomainClassifier

    classifier = DomainClassifier()
    result = classifier.classify_anchors(anchors)
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field


@dataclass
class DomainClassification:
    """Classification result for a single anchor."""
    anchor_id: str
    primary_domain: str
    primary_domain_id: int
    confidence: float
    secondary_domains: List[Tuple[str, float]] = field(default_factory=list)
    matched_keywords: List[str] = field(default_factory=list)


@dataclass
class ClassificationResult:
    """Container for classification results."""
    total_anchors: int
    classifications: List[DomainClassification] = field(default_factory=list)
    domain_distribution: Dict[str, int] = field(default_factory=dict)
    unclassified_anchors: List[str] = field(default_factory=list)
    metrics: Dict = field(default_factory=dict)


class DomainClassifier:
    """Classify content into NCLEX domains."""

    # Domain definitions with keywords
    DOMAINS = {
        'fundamentals': {
            'id': 1,
            'name': 'Fundamentals of Nursing',
            'keywords': [
                'vital signs', 'documentation', 'charting', 'nursing process',
                'assessment', 'basic care', 'hygiene', 'mobility', 'safety',
                'communication', 'patient education', 'infection control',
                'sterile technique', 'hand hygiene', 'isolation', 'restraints',
                'fall prevention', 'positioning', 'body mechanics', 'transfer',
                'admission', 'discharge', 'delegation', 'supervision', 'ethics',
                'legal', 'consent', 'advance directive', 'privacy', 'hipaa',
                'cultural', 'spiritual', 'end of life', 'palliative', 'hospice',
                'pain management', 'comfort', 'sleep', 'nutrition', 'hydration',
                'elimination', 'urinary', 'bowel', 'catheter', 'ostomy',
                'wound care', 'dressing', 'pressure ulcer', 'skin integrity',
                'oxygenation', 'oxygen therapy', 'suction', 'tracheostomy'
            ]
        },
        'pharmacology': {
            'id': 2,
            'name': 'Pharmacology',
            'keywords': [
                'medication', 'drug', 'pharmacology', 'pharmacokinetics',
                'pharmacodynamics', 'absorption', 'distribution', 'metabolism',
                'excretion', 'half-life', 'therapeutic', 'adverse effect',
                'side effect', 'contraindication', 'interaction', 'toxicity',
                'overdose', 'antidote', 'dose', 'dosage', 'route',
                'oral', 'sublingual', 'injectable', 'intravenous', 'intramuscular',
                'subcutaneous', 'topical', 'transdermal', 'inhalation',
                'antibiotic', 'antiviral', 'antifungal', 'analgesic', 'opioid',
                'nsaid', 'anticoagulant', 'antihypertensive', 'diuretic',
                'cardiac glycoside', 'antiarrhythmic', 'vasodilator', 'vasoconstrictor',
                'bronchodilator', 'corticosteroid', 'insulin', 'antidiabetic',
                'anticonvulsant', 'antidepressant', 'antipsychotic', 'anxiolytic',
                'sedative', 'hypnotic', 'antiemetic', 'laxative', 'antidiarrheal',
                'chemotherapy', 'immunosuppressant', 'vaccine', 'immunization'
            ]
        },
        'medical_surgical': {
            'id': 3,
            'name': 'Medical-Surgical Nursing',
            'keywords': [
                'cardiac', 'cardiovascular', 'heart', 'myocardial', 'coronary',
                'arrhythmia', 'dysrhythmia', 'hypertension', 'hypotension',
                'heart failure', 'chf', 'angina', 'mi', 'stroke', 'cva',
                'respiratory', 'pulmonary', 'copd', 'asthma', 'pneumonia',
                'tuberculosis', 'lung cancer', 'pleural', 'pneumothorax',
                'renal', 'kidney', 'dialysis', 'ckd', 'aki', 'uti',
                'gastrointestinal', 'gi', 'liver', 'hepatic', 'cirrhosis',
                'pancreatitis', 'gallbladder', 'cholecystitis', 'appendicitis',
                'crohn', 'colitis', 'ulcer', 'gerd', 'bowel obstruction',
                'endocrine', 'diabetes', 'thyroid', 'adrenal', 'pituitary',
                'musculoskeletal', 'fracture', 'arthritis', 'osteoporosis',
                'amputation', 'joint replacement', 'cast', 'traction',
                'neurological', 'seizure', 'epilepsy', 'parkinson', 'alzheimer',
                'dementia', 'multiple sclerosis', 'spinal cord', 'traumatic brain',
                'cancer', 'oncology', 'tumor', 'malignancy', 'radiation',
                'immune', 'hiv', 'aids', 'autoimmune', 'lupus',
                'perioperative', 'preoperative', 'intraoperative', 'postoperative',
                'surgery', 'anesthesia', 'wound', 'drainage', 'incision'
            ]
        },
        'ob_maternity': {
            'id': 4,
            'name': 'OB/Maternity Nursing',
            'keywords': [
                'pregnancy', 'pregnant', 'prenatal', 'antepartum', 'antenatal',
                'gestation', 'trimester', 'fetal', 'fetus', 'embryo',
                'conception', 'fertilization', 'implantation', 'placenta',
                'amniotic', 'umbilical', 'labor', 'delivery', 'birth',
                'intrapartum', 'contraction', 'cervical', 'dilation', 'effacement',
                'station', 'presentation', 'position', 'engagement', 'rupture',
                'cesarean', 'c-section', 'vaginal', 'episiotomy', 'laceration',
                'postpartum', 'puerperium', 'lochia', 'involution', 'breastfeeding',
                'lactation', 'breast milk', 'newborn', 'neonate', 'apgar',
                'preterm', 'premature', 'gestational age', 'small for gestational',
                'large for gestational', 'intrauterine', 'ectopic', 'miscarriage',
                'abortion', 'preeclampsia', 'eclampsia', 'hellp', 'gestational diabetes',
                'placenta previa', 'placental abruption', 'postpartum hemorrhage',
                'rh incompatibility', 'jaundice', 'hyperbilirubinemia', 'phototherapy',
                'maternal', 'obstetric', 'gynecologic', 'reproductive'
            ]
        },
        'pediatric': {
            'id': 5,
            'name': 'Pediatric Nursing',
            'keywords': [
                'pediatric', 'child', 'children', 'infant', 'toddler',
                'preschool', 'school age', 'adolescent', 'teen', 'growth',
                'development', 'milestone', 'immunization', 'vaccination',
                'well child', 'pediatric assessment', 'weight', 'height',
                'head circumference', 'fontanel', 'teething', 'eruption',
                'failure to thrive', 'developmental delay', 'autism', 'adhd',
                'cerebral palsy', 'down syndrome', 'congenital', 'birth defect',
                'cleft lip', 'cleft palate', 'clubfoot', 'hip dysplasia',
                'pyloric stenosis', 'intussusception', 'hirschsprung',
                'kawasaki', 'juvenile', 'rheumatic fever', 'cystic fibrosis',
                'asthma pediatric', 'bronchiolitis', 'rsv', 'croup', 'epiglottitis',
                'pertussis', 'measles', 'mumps', 'rubella', 'varicella',
                'hand foot mouth', 'roseola', 'scarlet fever', 'strep',
                'otitis media', 'tonsillitis', 'meningitis pediatric',
                'leukemia pediatric', 'wilms tumor', 'neuroblastoma',
                'sickle cell pediatric', 'hemophilia', 'iron deficiency',
                'lead poisoning', 'poisoning', 'child abuse', 'neglect',
                'sudden infant death', 'sids', 'colic', 'reflux infant'
            ]
        },
        'mental_health': {
            'id': 6,
            'name': 'Mental Health Nursing',
            'keywords': [
                'mental health', 'psychiatric', 'nursing', 'psychosis',
                'depression', 'anxiety', 'panic', 'phobia', 'ocd',
                'obsessive compulsive', 'ptsd', 'trauma', 'stress',
                'bipolar', 'mania', 'manic', 'mood', 'affect',
                'schizophrenia', 'hallucination', 'delusion', 'paranoia',
                'personality disorder', 'borderline', 'antisocial', 'narcissistic',
                'eating disorder', 'anorexia', 'bulimia', 'binge',
                'substance abuse', 'addiction', 'alcohol', 'drug abuse',
                'withdrawal', 'detoxification', 'rehabilitation',
                'suicide', 'suicidal', 'self-harm', 'crisis intervention',
                'therapeutic communication', 'milieu', 'group therapy',
                'cognitive behavioral', 'cbt', 'electroconvulsive', 'ect',
                'restraint', 'seclusion', 'involuntary', 'commitment',
                'psychotropic', 'antidepressant mental', 'antipsychotic mental',
                'mood stabilizer', 'lithium', 'benzodiazepine',
                'defense mechanism', 'coping', 'grief', 'loss',
                'dementia psychiatric', 'delirium', 'confusion acute'
            ]
        }
    }

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the DomainClassifier.

        Args:
            config_path: Optional path to nclex.yaml config
        """
        self.config_path = config_path
        self._load_config()

    def _load_config(self):
        """Load domain configuration from nclex.yaml if available."""
        try:
            from skills.utilities.yaml_parser import YAMLParser
            base_path = Path(__file__).parent.parent.parent

            parser = YAMLParser(str(base_path))
            result = parser.load("config/nclex.yaml")

            if result.success:
                domains_config = result.data.get('content', {}).get('domains', {})
                # Could enhance DOMAINS with config data here
        except Exception:
            pass

    def classify_anchor(self, anchor: Dict) -> DomainClassification:
        """
        Classify a single anchor into NCLEX domain.

        Args:
            anchor: Anchor dictionary with id, title, full_text

        Returns:
            DomainClassification result
        """
        anchor_id = anchor.get('id', 'unknown')
        title = anchor.get('title', '').lower()
        content = anchor.get('full_text', '').lower()
        full_text = f"{title} {content}"

        # Score each domain
        domain_scores = {}
        matched_keywords = {}

        for domain_key, domain_info in self.DOMAINS.items():
            keywords = domain_info['keywords']
            matches = []

            for keyword in keywords:
                if keyword in full_text:
                    matches.append(keyword)
                    # Weight title matches higher
                    if keyword in title:
                        matches.append(keyword)  # Double count

            domain_scores[domain_key] = len(matches)
            matched_keywords[domain_key] = matches

        # Find primary domain
        if not any(domain_scores.values()):
            # No matches - default to fundamentals
            return DomainClassification(
                anchor_id=anchor_id,
                primary_domain='fundamentals',
                primary_domain_id=1,
                confidence=0.3,
                secondary_domains=[],
                matched_keywords=[]
            )

        # Sort by score
        sorted_domains = sorted(
            domain_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        primary_domain = sorted_domains[0][0]
        primary_score = sorted_domains[0][1]
        total_score = sum(domain_scores.values())

        # Calculate confidence
        confidence = primary_score / total_score if total_score > 0 else 0

        # Get secondary domains
        secondary = []
        for domain, score in sorted_domains[1:3]:
            if score > 0:
                secondary.append((domain, score / total_score if total_score > 0 else 0))

        return DomainClassification(
            anchor_id=anchor_id,
            primary_domain=primary_domain,
            primary_domain_id=self.DOMAINS[primary_domain]['id'],
            confidence=min(1.0, confidence),
            secondary_domains=secondary,
            matched_keywords=matched_keywords[primary_domain][:5]
        )

    def classify_anchors(self, anchors: List[Dict]) -> ClassificationResult:
        """
        Classify multiple anchors.

        Args:
            anchors: List of anchor dictionaries

        Returns:
            ClassificationResult with all classifications
        """
        classifications = []
        domain_distribution = {domain: 0 for domain in self.DOMAINS}
        unclassified = []

        for anchor in anchors:
            classification = self.classify_anchor(anchor)
            classifications.append(classification)

            if classification.confidence >= 0.3:
                domain_distribution[classification.primary_domain] += 1
            else:
                unclassified.append(classification.anchor_id)

        # Calculate metrics
        total = len(anchors)
        classified = total - len(unclassified)

        metrics = {
            'classification_rate': classified / total * 100 if total > 0 else 0,
            'avg_confidence': sum(c.confidence for c in classifications) / total if total > 0 else 0,
            'primary_domain': max(domain_distribution.items(), key=lambda x: x[1])[0] if domain_distribution else 'none',
            'domain_count': sum(1 for v in domain_distribution.values() if v > 0)
        }

        return ClassificationResult(
            total_anchors=total,
            classifications=classifications,
            domain_distribution=domain_distribution,
            unclassified_anchors=unclassified,
            metrics=metrics
        )

    def get_domain_info(self, domain_key: str) -> Dict:
        """Get information about a domain."""
        return self.DOMAINS.get(domain_key, {})

    def get_all_domains(self) -> List[Dict]:
        """Get list of all domains with info."""
        return [
            {
                'key': key,
                'id': info['id'],
                'name': info['name'],
                'keyword_count': len(info['keywords'])
            }
            for key, info in self.DOMAINS.items()
        ]

    def format_report(self, result: ClassificationResult) -> str:
        """Format classification result as report."""
        lines = [
            "=" * 60,
            "DOMAIN CLASSIFICATION REPORT",
            "=" * 60,
            f"Total Anchors: {result.total_anchors}",
            f"Classification Rate: {result.metrics.get('classification_rate', 0):.1f}%",
            f"Average Confidence: {result.metrics.get('avg_confidence', 0):.2f}",
            ""
        ]

        lines.append("-" * 60)
        lines.append("DOMAIN DISTRIBUTION:")
        for domain, count in sorted(result.domain_distribution.items(), key=lambda x: x[1], reverse=True):
            domain_name = self.DOMAINS[domain]['name']
            percentage = count / result.total_anchors * 100 if result.total_anchors > 0 else 0
            bar = "#" * int(percentage / 5)
            lines.append(f"  {domain_name[:25]:<25} {count:>3} ({percentage:>5.1f}%) {bar}")

        lines.append("")
        lines.append("-" * 60)
        lines.append("SAMPLE CLASSIFICATIONS:")
        for classification in result.classifications[:5]:
            domain_name = self.DOMAINS[classification.primary_domain]['name']
            lines.append(f"  {classification.anchor_id}: {domain_name}")
            lines.append(f"    Confidence: {classification.confidence:.2f}")
            if classification.matched_keywords:
                lines.append(f"    Keywords: {', '.join(classification.matched_keywords[:3])}")

        if result.unclassified_anchors:
            lines.append("")
            lines.append(f"Unclassified ({len(result.unclassified_anchors)}): "
                        f"{', '.join(result.unclassified_anchors[:5])}")

        lines.append("")
        lines.append("=" * 60)
        return "\n".join(lines)


def classify_anchors(anchors: List[Dict]) -> ClassificationResult:
    """Convenience function to classify anchors."""
    classifier = DomainClassifier()
    return classifier.classify_anchors(anchors)


if __name__ == "__main__":
    print("Domain Classifier - NCLEX Pipeline Generation Skill")
    print("=" * 50)

    classifier = DomainClassifier()

    # Demo with sample anchors
    sample_anchors = [
        {'id': 'a1', 'title': 'Vital Signs Assessment', 'full_text': 'Temperature, pulse, respiration, blood pressure measurement...'},
        {'id': 'a2', 'title': 'Cardiac Medication Administration', 'full_text': 'Digoxin, beta blockers, ACE inhibitors dosing...'},
        {'id': 'a3', 'title': 'Heart Failure Management', 'full_text': 'CHF symptoms, treatment, nursing interventions...'},
        {'id': 'a4', 'title': 'Antepartum Assessment', 'full_text': 'Prenatal care, fetal monitoring, pregnancy complications...'},
        {'id': 'a5', 'title': 'Pediatric Growth and Development', 'full_text': 'Child milestones, infant development stages...'},
        {'id': 'a6', 'title': 'Depression and Anxiety', 'full_text': 'Mental health assessment, therapeutic communication...'},
        {'id': 'a7', 'title': 'Insulin Administration', 'full_text': 'Diabetes medication, injection technique, monitoring...'},
        {'id': 'a8', 'title': 'Wound Care Documentation', 'full_text': 'Wound assessment, dressing changes, charting...'},
    ]

    print("\nClassifying anchors...")
    result = classifier.classify_anchors(sample_anchors)

    report = classifier.format_report(result)
    print(report)
