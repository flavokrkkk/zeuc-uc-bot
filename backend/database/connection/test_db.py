from random import choice
from numpy.f2py.symbolic import as_eq
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.models.models import Discount, Price, Reward, Setting, User, UserDiscounts
from backend.database.models.models import UCCode


async def test_db(session):
    try:
        db_exist = (await session.execute(select(UCCode))).scalars().all()
        if db_exist:
            await session.close()
            return
        
        mago = User(tg_id=5163648472, username="magoxdd", is_admin=True, bonuses=200)
        mago = User(tg_id=5163648472, username="magoxdd", is_admin=True, bonuses=1000000)
        setting = Setting(store_is_on=True)
        
        uc_codes_values = {60: [100, 1], 325: [200, 4], 660: [300, 5], 1800: [2000, 8], 3850: [5500, 10], 8100: [10000, 20]}
        
        uc_codes = []
        rewards = []
        for key, value in uc_codes_values.items():
            uc_codes.append(
            UCCode(
                code=f"uc_code_{value}", 
                uc_amount=key, 
                price_per_uc=Price(
                    price=value[0], 
                    point=value[1]
                )
            )
        )
        for uc_code in list(uc_codes_values.keys())[:3]:
            rewards.append(
                Reward(
                    reward_type="uc_code",
                    uc_amount=uc_code
                )
            )
        
        discounts = {100: 1000, 200: 2000, 300: 300, 500: 5000}
        for key, value in discounts.items():
            rewards.append(
                Reward(
                    reward_type="discount", 
                    discount=Discount(
                        value=key, 
                        min_payment_value=value
                    )
                )
            )
        
        for i in range(100):
            session.add(
                User(
                    tg_id=i,
                    username=f"test_{i}",
                    in_black_list=False,
                    bonuses=30
                )
            )
        session.add_all(rewards)
        await session.commit()
        for i in range(100):
            session.add(UserDiscounts(user_id=i, discount_id=choice(range(1, 4))))

        session.add_all(uc_codes)
        session.add(mago)
        session.add(setting)
        await session.commit()
        await session.close()
    except Exception as e:
        print(e)
    finally:
        await session.close()


async def test_admins(session: AsyncSession):
    try:
        zeuc_nis = await session.get(User, 5718861071)
        if not zeuc_nis:
            zeuc_nis = User(tg_id=5718861071, username="zeucNIS", is_admin=True, bonuses=200)
            session.add(zeuc_nis)
        zeuc_uc = await session.get(User, 494055871)
        if not zeuc_uc:
            zeuc_uc = User(tg_id=494055871, username="zeucUC", is_admin=True, bonuses=200)
            session.add(zeuc_uc)
        await session.commit()
    except Exception as e:
        pass
    finally:
        await session.close()