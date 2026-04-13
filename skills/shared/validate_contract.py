#!/usr/bin/env python3
"""
Contract Validation Script
Validates skill contracts against the contract schema
"""

import json
import sys
from pathlib import Path
from jsonschema import validate, ValidationError

def validate_contract(contract_path: Path, schema_path: Path) -> tuple[bool, str]:
    """
    Validate a skill contract against the schema

    Args:
        contract_path: Path to contract JSON file
        schema_path: Path to contract schema JSON file

    Returns:
        (is_valid, error_message)
    """
    try:
        with open(schema_path) as f:
            schema = json.load(f)

        with open(contract_path) as f:
            contract = json.load(f)

        validate(instance=contract, schema=schema)

        # Additional validation: check skill name matches filename
        expected_skill = contract_path.stem
        if contract['skill'] != expected_skill:
            return False, f"Skill name '{contract['skill']}' doesn't match filename '{expected_skill}'"

        return True, ""

    except ValidationError as e:
        return False, f"Schema validation error: {e.message}"
    except json.JSONDecodeError as e:
        return False, f"JSON parsing error: {e.msg}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def main():
    """Validate all contracts in skills/contracts/"""
    skills_dir = Path(__file__).parent.parent
    schema_path = skills_dir / "schemas" / "contract.schema.json"
    contracts_dir = skills_dir / "contracts"

    if not schema_path.exists():
        print(f"❌ Schema not found: {schema_path}")
        sys.exit(1)

    if not contracts_dir.exists():
        print(f"❌ Contracts directory not found: {contracts_dir}")
        sys.exit(1)

    contracts = list(contracts_dir.glob("*.json"))

    if len(contracts) == 0:
        print(f"❌ No contracts found in {contracts_dir}")
        sys.exit(1)

    print(f"Validating {len(contracts)} contracts against schema...")
    print()

    all_valid = True
    for contract_path in sorted(contracts):
        is_valid, error = validate_contract(contract_path, schema_path)

        if is_valid:
            print(f"✓ {contract_path.name}")
            # Print contract summary
            with open(contract_path) as f:
                contract = json.load(f)
            requires_count = len(contract['requires'])
            produces_count = len(contract['produces'])
            gates_count = len(contract['gates'])
            print(f"  Requires: {requires_count}, Produces: {produces_count}, Gates: {gates_count}")
        else:
            print(f"✗ {contract_path.name}")
            print(f"  Error: {error}")
            all_valid = False

    print()
    if all_valid:
        print(f"✓ All {len(contracts)} contracts valid")
        sys.exit(0)
    else:
        print(f"✗ Some contracts invalid")
        sys.exit(1)

if __name__ == "__main__":
    main()