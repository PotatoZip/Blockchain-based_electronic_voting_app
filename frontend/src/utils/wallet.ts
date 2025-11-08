import { Wallet } from "ethers";

const KEYSTORE_KEY = "evote_keystore";

// In-memory password cache (cleared when page reloads)
let memoryPasswordCache: string | null = null;

// By default we cache the password in memory only (cleared when the page reloads).
// This avoids prompting the user repeatedly during the current page session while ensuring
// the password is never stored in any browser storage.
async function defaultPasswordGetter(): Promise<string> {
  if (memoryPasswordCache) return memoryPasswordCache;
  const p = prompt("Enter wallet password:");
  if (!p) throw new Error("Password is required");
  memoryPasswordCache = p;
  return p;
}

export async function ensureWallet(
  passwordGetter?: () => Promise<string>
): Promise<Wallet> {
  const pwGetter = passwordGetter ?? defaultPasswordGetter;
  const existing = localStorage.getItem(KEYSTORE_KEY);
  if (existing) {
    const pass = await pwGetter();
    try {
      const w = (await Wallet.fromEncryptedJson(
        existing,
        pass
      )) as unknown as Wallet;
      return w;
    } catch (error) {
      // Clear the cached password since it was wrong
      memoryPasswordCache = null;
      throw new Error("You entered wrong wallet password");
    }
  }
  // brak portfela – generujemy
  const wallet = Wallet.createRandom() as unknown as Wallet;
  const pass = await pwGetter();
  const json = await wallet.encrypt(pass);
  localStorage.setItem(KEYSTORE_KEY, json);
  return wallet;
}

export async function getAddress(
  passwordGetter?: () => Promise<string>
): Promise<string> {
  const w = await ensureWallet(passwordGetter);
  return w.address;
}

export async function signMessage(
  message: string,
  passwordGetter?: () => Promise<string>
): Promise<{ signature: string; address: string }> {
  const wallet = await ensureWallet(passwordGetter);
  const sig = await wallet.signMessage(message);
  return { signature: sig, address: wallet.address };
}

/**
 * Clear cached memory password (keeps keystore JSON in localStorage).
 * Use when user explicitly logs out of the session but wants to keep the keystore.
 */
export function clearWalletSession(): void {
  memoryPasswordCache = null;
}

/**
 * Remove keystore and memory password (full logout / remove wallet from browser).
 */
export function clearWallet(): void {
  memoryPasswordCache = null;
  try {
    localStorage.removeItem(KEYSTORE_KEY);
  } catch (e) {
    // ignore
  }
}

/**
 * Reset wallet for new election. This will remove the existing wallet
 * and allow generation of a new one with a new password.
 * Only use this when explicitly requested by the user and confirmed
 * that they understand the consequences.
 */
export async function resetWalletForNewElection(): Promise<void> {
  // Clear everything
  clearWallet();

  // Force new wallet generation on next ensure
  const wallet = await ensureWallet();
  return;
}
