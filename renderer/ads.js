'use strict'
/**
 * MahiraClipper — Ad Manager
 * Sistem iklan affiliate yang bisa di-close, rotasi otomatis,
 * dan muncul di konteks yang tepat (splash, processing, done, about).
 *
 * Edit /ads.json untuk ganti iklan — tidak perlu coding!
 */

const AdManager = (() => {
  let ADS_DATA    = { settings: {}, ads: [] }
  let currentAd   = null
  let rotateTimer = null
  let closeTimer  = null
  let clickLog    = {}   // { ad_id: count } — simpan di memory
  let currentCtx  = null

  // ── Load data iklan ───────────────────────────────────────────────────────
  async function init() {
    try {
      const data = await window.app.getAds()
      if (data && data.ads) ADS_DATA = data
    } catch (e) {
      console.warn('Ads load failed:', e)
    }
  }

  // ── Ambil iklan sesuai platform ───────────────────────────────────────────
  function getAdsFor(platform) {
    return ADS_DATA.ads.filter(a =>
      a.active !== false &&
      Array.isArray(a.platforms) &&
      a.platforms.includes(platform)
    )
  }

  // ── Render satu iklan ke dalam container ─────────────────────────────────
  function renderAd(ad, container) {
    if (!ad || !container) return
    currentAd = ad

    const settings   = ADS_DATA.settings || {}
    const minClose   = (settings.min_close_after_sec || 3) * 1000
    const hasImage   = ad.image && ad.image.length > 3

    container.innerHTML = `
      <div class="ad-inner" id="ad-inner-${ad.id}">
        <div class="ad-close-wrap">
          <span class="ad-sponsored-label">Sponsor</span>
          <button class="ad-close-btn" id="ad-close-btn" title="Tutup iklan">
            <svg width="10" height="10" viewBox="0 0 10 10">
              <line x1="1" y1="1" x2="9" y2="9" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
              <line x1="9" y1="1" x2="1" y2="9" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
            </svg>
          </button>
        </div>
        <div class="ad-body" id="ad-body-click">
          ${hasImage
            ? `<div class="ad-img-wrap"><img src="${ad.image}" alt="" class="ad-img" onerror="this.parentElement.style.display='none'"></div>`
            : `<div class="ad-emoji-wrap" style="background:${ad.image_fallback_bg || '#f0f0f0'}">${ad.image_fallback_emoji || '📢'}</div>`
          }
          <div class="ad-text">
            <div class="ad-title">${esc(ad.title || '')}</div>
            <div class="ad-desc">${esc(ad.description || '')}</div>
          </div>
          <div class="ad-cta-wrap">
            <span class="ad-label" style="color:${ad.label_color || '#666'}">${esc(ad.label || '')}</span>
            <button class="ad-cta-btn">${esc(ad.cta || 'Lihat →')}</button>
          </div>
        </div>
        <div class="ad-close-timer" id="ad-close-timer"></div>
      </div>
    `

    // Close button — bisa tutup setelah min_close detik
    const closeBtn   = container.querySelector('#ad-close-btn')
    const timerEl    = container.querySelector('#ad-close-timer')
    let   canClose   = false

    // Timer countdown sebelum boleh close
    let remaining = Math.ceil(minClose / 1000)
    timerEl.textContent = `Tutup dalam ${remaining}s`
    closeBtn.style.opacity = '0.3'
    closeBtn.style.cursor  = 'not-allowed'

    clearInterval(closeTimer)
    closeTimer = setInterval(() => {
      remaining--
      if (remaining > 0) {
        timerEl.textContent = `Tutup dalam ${remaining}s`
      } else {
        clearInterval(closeTimer)
        timerEl.textContent = ''
        canClose = true
        closeBtn.style.opacity = '1'
        closeBtn.style.cursor  = 'pointer'
      }
    }, 1000)

    closeBtn.onclick = (e) => {
      e.stopPropagation()
      if (!canClose) return
      hideAd(container)
    }

    // Click iklan → buka URL
    const bodyEl = container.querySelector('#ad-body-click')
    const ctaBtn = container.querySelector('.ad-cta-btn')
    const clickFn = () => openAd(ad)
    bodyEl?.addEventListener('click', clickFn)
    ctaBtn?.addEventListener('click', (e) => { e.stopPropagation(); clickFn() })

    // Animasi masuk
    container.classList.remove('ad-hidden')
    container.classList.add('ad-visible')
    setTimeout(() => container.querySelector('.ad-inner')?.classList.add('ad-enter'), 50)
  }

  function openAd(ad) {
    if (!ad.url) return
    // Track click
    clickLog[ad.id] = (clickLog[ad.id] || 0) + 1
    console.log(`[Ad] Clicked: ${ad.id} (total: ${clickLog[ad.id]})`)
    window.app.openUrl(ad.url)
  }

  function hideAd(container) {
    if (!container) return
    container.classList.remove('ad-visible')
    container.classList.add('ad-hidden')
    clearInterval(rotateTimer)
    clearInterval(closeTimer)
  }

  // ── Show iklan untuk konteks tertentu ────────────────────────────────────
  function show(platform, containerId) {
    const container = document.getElementById(containerId)
    if (!container) return

    const ads = getAdsFor(platform)
    if (!ads.length) { container.classList.add('ad-hidden'); return }

    currentCtx = { platform, containerId, ads, idx: 0 }
    const settings = ADS_DATA.settings || {}

    // Delay sebelum muncul
    const delay = (settings.show_after_sec || 2) * 1000
    setTimeout(() => {
      renderAd(ads[0], container)

      // Rotasi otomatis
      const interval = (settings.rotate_interval_sec || 8) * 1000
      clearInterval(rotateTimer)
      rotateTimer = setInterval(() => {
        currentCtx.idx = (currentCtx.idx + 1) % ads.length
        renderAd(ads[currentCtx.idx], container)
      }, interval)
    }, delay)
  }

  function hide(containerId) {
    hideAd(document.getElementById(containerId))
  }

  function esc(s) {
    return String(s || '')
      .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
  }

  return { init, show, hide, getAdsFor }
})()

window.AdManager = AdManager
