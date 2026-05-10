#!/usr/bin/env bash
# =============================================================================
# deploy.sh — Déploiement automatisé de la plateforme E-Commerce DevNet
# Usage : ./deploy.sh
# Prérequis : Docker et Docker Compose installés
# =============================================================================

set -e

# ── Couleurs ──────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; BLUE='\033[0;34m'; RED='\033[0;31m'; NC='\033[0m'

log()  { echo -e "${BLUE}[INFO]${NC}  $1"; }
ok()   { echo -e "${GREEN}[ OK ]${NC}  $1"; }
fail() { echo -e "${RED}[FAIL]${NC}  Échec à l'étape : $1"; exit 1; }

echo "============================================================"
log "Démarrage du déploiement E-Commerce DevNet..."
echo "============================================================"

# ── Vérifications préalables ──────────────────────────────────────────────────
command -v docker        >/dev/null 2>&1 || fail "Docker non installé"
command -v docker compose >/dev/null 2>&1 || fail "Docker Compose non installé"
ok "Docker et Docker Compose disponibles"

# ── Étape 1 : Build des images ────────────────────────────────────────────────
log "Étape 1/2 — Construction des images Docker..."
docker compose build || fail "Construction des images"
ok "Images construites"

# ── Étape 2 : Démarrage des services ─────────────────────────────────────────
log "Étape 2/2 — Démarrage des services..."
docker compose up -d || fail "Démarrage des services"
ok "Services démarrés"

# ── Résultat ──────────────────────────────────────────────────────────────────
echo ""
echo "============================================================"
ok "Déploiement terminé avec succès !"
echo ""
echo -e "  ${GREEN}Frontend  :${NC}  http://localhost:80"
echo -e "  ${GREEN}API       :${NC}  http://localhost:8000"
echo -e "  ${GREEN}API Docs  :${NC}  http://localhost:8000/docs"
echo "============================================================"
