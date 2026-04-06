import { PokemonSlot } from "./types";

const SPECIES_IMAGE_SLUGS: Record<string, string> = {
  "ogerpon-w": "ogerpon-wellspring",
  "ogerpon-h": "ogerpon-hearthflame",
  "ogerpon-c": "ogerpon-cornerstone",
  "bloodmoon ursaluna": "ursaluna-bloodmoon",
  "ursaluna bloodmoon": "ursaluna-bloodmoon",
  landorus: "landorus-therian",
  "landorus-t": "landorus-therian"
};

const SPECIES_DISPLAY_ALIASES: Record<string, string> = {
  "ogerpon-w": "Ogerpon-Wellspring",
  "ogerpon-h": "Ogerpon-Hearthflame",
  "ogerpon-c": "Ogerpon-Cornerstone",
  "bloodmoon ursaluna": "Ursaluna-Bloodmoon",
  "ursaluna bloodmoon": "Ursaluna-Bloodmoon",
  landorus: "Landorus-Therian",
  "landorus-t": "Landorus-Therian"
};

function toPokemonKey(name: string): string {
  return name
    .trim()
    .toLowerCase()
    .replaceAll(".", "")
    .replaceAll("'", "")
    .replaceAll("♀", "-f")
    .replaceAll("♂", "-m")
    .replace(/[_\s]+/g, " ")
    .replace(/[^a-z0-9 -]+/g, "")
    .trim();
}

export function slugifyPokemonSpecies(name: string): string {
  const trimmed = name.trim();
  const aliasKey = toPokemonKey(trimmed);

  if (SPECIES_IMAGE_SLUGS[aliasKey]) {
    return SPECIES_IMAGE_SLUGS[aliasKey];
  }

  return trimmed
    .toLowerCase()
    .replaceAll(".", "")
    .replaceAll("'", "")
    .replaceAll("♀", "-f")
    .replaceAll("♂", "-m")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

export function getPokemonSpeciesIdentity(name: string): string {
  const aliasKey = toPokemonKey(name);
  return SPECIES_IMAGE_SLUGS[aliasKey] ?? slugifyPokemonSpecies(name);
}

export function getPokemonSpeciesAliasHint(name: string): string {
  const trimmed = name.trim();
  const aliasKey = toPokemonKey(trimmed);
  const canonicalName = SPECIES_DISPLAY_ALIASES[aliasKey];

  if (!canonicalName || canonicalName.toLowerCase() === trimmed.toLowerCase()) {
    return "";
  }

  return `Uses ${canonicalName} for sprite lookup and duplicate checks.`;
}

export function getPokemonImageUrl(name: string): string {
  const slug = slugifyPokemonSpecies(name);
  if (!slug) {
    return "";
  }

  return `https://img.pokemondb.net/sprites/scarlet-violet/normal/${slug}.png`;
}

export function normalizePokemonSlot(member: PokemonSlot): PokemonSlot {
  const trimmedName = member.name.trim();

  return {
    ...member,
    name: trimmedName,
    item: member.item.trim(),
    ability: member.ability.trim(),
    role: member.role.trim(),
    teraType: member.teraType?.trim() || "",
    types: member.types.map((type) => type.trim()).filter(Boolean),
    moves: member.moves.map((move) => move.trim()).filter(Boolean),
    image: trimmedName ? getPokemonImageUrl(trimmedName) : ""
  };
}

export function getSmogonDexUrl(name: string): string {
  const slug = slugifyPokemonSpecies(name);
  return `https://www.smogon.com/dex/sv/pokemon/${slug}/vgc25-regulation-i/`;
}

export function getSmogonSearchUrl(name: string): string {
  return `https://www.smogon.com/search/?q=${encodeURIComponent(name)}`;
}
