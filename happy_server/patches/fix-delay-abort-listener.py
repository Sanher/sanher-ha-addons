#!/usr/bin/env python3
from pathlib import Path

path = Path('/opt/happy/packages/happy-server/sources/utils/delay.ts')
content = path.read_text(encoding='utf-8').replace('\r\n', '\n')

old = """    await new Promise<void>((resolve) => {
        const timeout = setTimeout(resolve, ms);

        const abortHandler = () => {
            clearTimeout(timeout);
            resolve();
        };

        if (signal.aborted) {
            clearTimeout(timeout);
            resolve();
        } else {
            signal.addEventListener('abort', abortHandler, { once: true });
        }
    });"""

new = """    await new Promise<void>((resolve) => {
        let settled = false;
        let abortHandler: () => void = () => {};

        const cleanup = () => signal.removeEventListener('abort', abortHandler);
        const resolveOnce = () => {
            if (settled) {
                return;
            }
            settled = true;
            cleanup();
            resolve();
        };

        const timeout = setTimeout(resolveOnce, ms);

        abortHandler = () => {
            clearTimeout(timeout);
            resolveOnce();
        };

        if (signal.aborted) {
            clearTimeout(timeout);
            resolveOnce();
        } else {
            signal.addEventListener('abort', abortHandler, { once: true });
        }
    });"""

if old not in content:
    raise SystemExit('No se pudo localizar el bloque esperado en delay.ts para aplicar el fix de listeners abort')

path.write_text(content.replace(old, new, 1), encoding='utf-8')
print('Patched delay.ts abort listener cleanup')
